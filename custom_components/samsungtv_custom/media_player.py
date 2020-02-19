"""Support for interface with an Samsung TV."""
import asyncio
from datetime import timedelta
import logging
import socket
import json
import voluptuous as vol
import os
import wakeonlan
import websocket
import requests
import time

from samsungtvws import SamsungTVWS

from homeassistant import util
from homeassistant.components.media_player import MediaPlayerDevice, PLATFORM_SCHEMA
from homeassistant.components.media_player.const import (
    MEDIA_TYPE_CHANNEL,
    SUPPORT_NEXT_TRACK,
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_PLAY_MEDIA,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_SELECT_SOURCE,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    SUPPORT_VOLUME_MUTE,
    SUPPORT_VOLUME_STEP,
    MEDIA_TYPE_APP,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_MAC,
    CONF_NAME,
    CONF_PORT,
    CONF_TIMEOUT,
    STATE_OFF,
    STATE_ON,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Samsung TV Remote"
DEFAULT_PORT = 8001
DEFAULT_TIMEOUT = 1.5
DEFAULT_UPDATE_METHOD = "default"
DEFAULT_SOURCE_LIST = '{"TV": "KEY_TV", "HDMI": "KEY_HDMI_FIX"}'
CONF_UPDATE_METHOD = "update_method"
CONF_UPDATE_CUSTOM_PING_URL = "update_custom_ping_url"
CONF_SOURCE_LIST = "source_list"
CONF_APP_LIST = "app_list"

KNOWN_DEVICES_KEY = "samsungtv_known_devices"
MEDIA_TYPE_KEY = "send_key"
KEY_PRESS_TIMEOUT = 0.3
UPDATE_PING_TIMEOUT = 1
MIN_TIME_BETWEEN_FORCED_SCANS = timedelta(seconds=1)
MIN_TIME_BETWEEN_SCANS = timedelta(seconds=10)

SUPPORT_SAMSUNGTV = (
    SUPPORT_PAUSE
    | SUPPORT_VOLUME_STEP
    | SUPPORT_VOLUME_MUTE
    | SUPPORT_PREVIOUS_TRACK
    | SUPPORT_SELECT_SOURCE
    | SUPPORT_NEXT_TRACK
    | SUPPORT_TURN_OFF
    | SUPPORT_PLAY
    | SUPPORT_PLAY_MEDIA
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_MAC): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
        vol.Optional(CONF_UPDATE_METHOD, default=DEFAULT_UPDATE_METHOD): cv.string,
        vol.Optional(CONF_UPDATE_CUSTOM_PING_URL): cv.string,
        vol.Optional(CONF_SOURCE_LIST, default=DEFAULT_SOURCE_LIST): cv.string,
        vol.Optional(CONF_APP_LIST): cv.string
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Samsung TV platform."""
    known_devices = hass.data.get(KNOWN_DEVICES_KEY)
    if known_devices is None:
        known_devices = set()
        hass.data[KNOWN_DEVICES_KEY] = known_devices

    uuid = None

    # Is this a manual configuration?
    if config.get(CONF_HOST) is not None:
        host = config.get(CONF_HOST)
        port = config.get(CONF_PORT)
        name = config.get(CONF_NAME)
        mac = config.get(CONF_MAC)
        timeout = config.get(CONF_TIMEOUT)
        update_method = config.get(CONF_UPDATE_METHOD)
        update_custom_ping_url = config.get(CONF_UPDATE_CUSTOM_PING_URL)
        source_list = config.get(CONF_SOURCE_LIST)
        app_list = config.get(CONF_APP_LIST)
    elif discovery_info is not None:
        tv_name = discovery_info.get("name")
        model = discovery_info.get("model_name")
        host = discovery_info.get("host")
        name = f"{tv_name} ({model})"
        port = DEFAULT_PORT
        timeout = DEFAULT_TIMEOUT
        update_method = DEFAULT_UPDATE_METHOD
        update_custom_ping_url = None
        source_list = DEFAULT_SOURCE_LIST
        app_list = None
        mac = None
        udn = discovery_info.get("udn")
        if udn and udn.startswith("uuid:"):
            uuid = udn[len("uuid:") :]
    else:
        _LOGGER.warning("Cannot determine device")
        return

    # Only add a device once, so discovered devices do not override manual
    # config.
    ip_addr = socket.gethostbyname(host)
    if ip_addr not in known_devices:
        known_devices.add(ip_addr)
        add_entities([SamsungTVDevice(host, port, name, timeout, mac, uuid, update_method, update_custom_ping_url, source_list, app_list)])
        _LOGGER.info("Samsung TV %s:%d added as '%s'", host, port, name)
    else:
        _LOGGER.info("Ignoring duplicate Samsung TV %s:%d", host, port)


class SamsungTVDevice(MediaPlayerDevice):
    """Representation of a Samsung TV."""

    def __init__(self, host, port, name, timeout, mac, uuid, update_method, update_custom_ping_url, source_list, app_list):
        """Initialize the Samsung device."""

        # Save a reference to the imported classes
        self._host = host
        self._name = name
        self._timeout = timeout
        self._mac = mac
        self._update_method = update_method
        self._update_custom_ping_url = update_custom_ping_url
        self._source_list = json.loads(source_list)
        self._app_list = json.loads(app_list) if app_list is not None else None
        self._uuid = uuid
        self._is_ws_connection = True if port in (8001, 8002) else False
        # Assume that the TV is not muted and volume is 0
        self._muted = False
        # Assume that the TV is in Play mode
        self._playing = True
        self._state = None
        # Mark the end of a shutdown command (need to wait 15 seconds before
        # sending the next command to avoid turning the TV back ON).
        self._end_of_power_off = None
        self._token_file = None

        # Generate token file only for WS + SSL + Token connection
        if port == 8002:
            self._gen_token_file()

        self._remote = SamsungTVWS(
            name=name,
            host=host,
            port=port,
            timeout=self._timeout,
            key_press_delay=KEY_PRESS_TIMEOUT,
            token_file=self._token_file
        )

    def _gen_token_file(self):
        self._token_file = os.path.dirname(os.path.realpath(__file__)) + '/token-' + self._host + '.txt'

        if os.path.isfile(self._token_file) is False:
            # For correct auth
            self._timeout = 45

            # Create token file for catch possible errors
            try :
                handle = open(self._token_file, "w+")
                handle.close()
            except:
                _LOGGER.error("Samsung TV - Error creating token file: %s", self._token_file)

    def _power_off_in_progress(self):
        return (
            self._end_of_power_off is not None
            and self._end_of_power_off > dt_util.utcnow()
        )

    def _ping_device(self):
        # HTTP ping
        if self._is_ws_connection and self._update_method == "ping":
            try:
                ping_url = "http://{}:8001/api/v2/".format(self._host)
                if self._update_custom_ping_url is not None:
                    ping_url = self._update_custom_ping_url

                requests.get(
                    ping_url,
                    timeout=UPDATE_PING_TIMEOUT
                )
                self._state = STATE_ON
            except:
                self._state = STATE_OFF

        # WS ping
        else:
            self.send_command("KEY", 1, 0)

    def _gen_installed_app_list(self):
        if self._state == STATE_OFF:
            _LOGGER.info("Samsung TV is OFF, _gen_installed_app_list not executed")
            self._app_list = {}

        app_list = self._remote.app_list()

        # app_list is a list of dict
        clean_app_list = {}
        for i in range(len(app_list)):
            try:
                app = app_list[i]
                clean_app_list[ app.get('name') ] = app.get('appId')
            except Exception:
                pass

        self._app_list = clean_app_list
        _LOGGER.debug("Gen installed app_list %s", clean_app_list)

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_FORCED_SCANS)
    def update(self):
        """Update state of device."""
        self._ping_device()

    def send_command(self, payload, command_type = "send_key", retry_count = 1):
        """Send a key to the tv and handles exceptions."""
        if self._power_off_in_progress() and payload not in ("KEY_POWER", "KEY_POWEROFF"):
            _LOGGER.info("TV is powering off, not sending command: %s", payload)
            return False

        try:
            # recreate connection if connection was dead
            for _ in range(retry_count + 1):
                try:
                    if command_type == "run_app":
                        #run_app(self, app_id, app_type='DEEP_LINK', meta_tag='')
                        self._remote.run_app(payload)
                    else:
                        times = 1

                        # fix KEY_HDMI ws error
                        if payload == "KEY_HDMI_FIX":
                            payload = "KEY_HDMI"
                            times = 2

                        self._remote.send_key(payload, times, 1)

                    break
                except (
                    ConnectionResetError, 
                    AttributeError, 
                    BrokenPipeError
                ):
                    self._remote.close()
                    _LOGGER.debug("Error in send_command() -> ConnectionResetError/AttributeError/BrokenPipeError")

            self._state = STATE_ON
        except websocket._exceptions.WebSocketTimeoutException:
            # We got a response so it's on.
            self._state = STATE_ON
            self._remote.close()
            _LOGGER.debug("Failed sending payload %s command_type %s", payload, command_type, exc_info=True)

        except OSError:
            self._state = STATE_OFF
            self._remote.close()
            _LOGGER.debug("Error in send_command() -> OSError")

        if self._power_off_in_progress():
            self._state = STATE_OFF

        return True

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the device."""
        return self._uuid

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def is_volume_muted(self):
        """Boolean if volume is currently muted."""
        return self._muted

    @property
    def source_list(self):
        """List of available input sources."""
        if self._app_list is None:
            self._gen_installed_app_list()

        source_list = []
        source_list.extend(list(self._source_list))
        source_list.extend(list(self._app_list))

        return source_list

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return SUPPORT_SAMSUNGTV | SUPPORT_TURN_ON

    def turn_on(self):
        """Turn the media player on."""
        if self._mac:
            if self._power_off_in_progress():
                _LOGGER.info("TV is powering off, not sending WOL")
                return

            wakeonlan.send_magic_packet(self._mac)
            time.sleep(2)
            self._ping_device()
        else:
            self.send_command("KEY_POWERON")

    def turn_off(self):
        """Turn off media player."""
        # In my tests if _end_of_power_off < 15 WS ping method randomly fail!!!
        self._end_of_power_off = dt_util.utcnow() + timedelta(seconds=15)

        if self._is_ws_connection:
            self.send_command("KEY_POWER")
        else:
            self.send_command("KEY_POWEROFF")

        # Force closing of remote session to provide instant UI feedback
        try:
            self._remote.close()
        except OSError:
            _LOGGER.debug("Could not establish connection.")

    def volume_up(self):
        """Volume up the media player."""
        self.send_command("KEY_VOLUP")

    def volume_down(self):
        """Volume down media player."""
        self.send_command("KEY_VOLDOWN")

    def mute_volume(self, mute):
        """Send mute command."""
        self.send_command("KEY_MUTE")

    def media_play_pause(self):
        """Simulate play pause media player."""
        if self._playing:
            self.media_pause()
        else:
            self.media_play()

    def media_play(self):
        """Send play command."""
        self._playing = True
        self.send_command("KEY_PLAY")

    def media_pause(self):
        """Send media pause command to media player."""
        self._playing = False
        self.send_command("KEY_PAUSE")

    def media_next_track(self):
        """Send next track command."""
        self.send_command("KEY_FF")

    def media_previous_track(self):
        """Send the previous track command."""
        self.send_command("KEY_REWIND")

    async def async_play_media(self, media_type, media_id, **kwargs):
        """Support changing a channel."""

        # Type channel
        if media_type == MEDIA_TYPE_CHANNEL:
            try:
                cv.positive_int(media_id.replace("-", "", 1))
                # Hyphen must be between numbers
                if media_id.startswith("-") or media_id.endswith("-"):
                    raise vol.Invalid("")
            except vol.Invalid:
                _LOGGER.error("Media ID must be channel with optional sub-channel, separated by a hyphen (ex. 20-2)")
                return

            for digit in media_id:
                await self.hass.async_add_job(self.send_command, "KEY_PLUS100" if digit == "-" else "KEY_" + digit)

            await self.hass.async_add_job(self.send_command, "KEY_ENTER")

        # Launch an app
        elif media_type == MEDIA_TYPE_APP:
            await self.hass.async_add_job(self.send_command, media_id, "run_app")

        # Send custom key
        elif media_type == MEDIA_TYPE_KEY:
            try:
                cv.string(media_id)
            except vol.Invalid:
                _LOGGER.error('Media ID must be a string (ex: "KEY_HOME"')
                return

            await self.hass.async_add_job(self.send_command, media_id)

        else:
            _LOGGER.error("Unsupported media type")
            return

    async def async_select_source(self, source):
        """Select input source."""
        if source in self._source_list:
            await self.hass.async_add_job(self.send_command, self._source_list[ source ])
        elif source in self._app_list:
            await self.hass.async_add_job(self.send_command, self._app_list[ source ], "run_app")
        else:
            _LOGGER.error("Unsupported source")
