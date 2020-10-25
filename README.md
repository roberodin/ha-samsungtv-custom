[![](https://img.shields.io/github/release/roberodin/ha-samsungtv-custom/all.svg?style=for-the-badge)](https://github.com/roberodin/ha-samsungtv-custom/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![](https://img.shields.io/github/license/roberodin/ha-samsungtv-custom?style=for-the-badge)](LICENSE)
[![](https://img.shields.io/badge/MAINTAINER-%40roberodin-red?style=for-the-badge)](https://github.com/roberodin)
[![](https://img.shields.io/badge/COMMUNITY-FORUM-success?style=for-the-badge)](https://community.home-assistant.io)

# HomeAssistant - SamsungTV Custom Component

This is a custom component to allow control of SamsungTV devices in [HomeAssistant](https://home-assistant.io). Is a modified version of the built-in [samsungtv](https://www.home-assistant.io/integrations/samsungtv/) with some extra features:

# Additional Features:

* Send keys using a native Home Assistant service
* Customize source list at media player dropdown list
* Change communication protocol to cover more compatibility TV models. Thanks to:
    - WS protocol from [@xchwarze](https://github.com/xchwarze/ha-samsungtv-custom)
    - Qled protocol from [@giefca](https://github.com/giefca/ha-samsungtv-qled)
    - Ctl beta from [@kdschlosser](https://github.com/kdschlosser/samsungctl)
* Launch applications and add them to the source list (only for Qled protocol)
* Launch streaming of music and video from files (not compatible with HA stream component, only for Qled protocol)

![N|Solid](https://i.imgur.com/8mCGZoO.png)
![N|Solid](https://i.imgur.com/t3e4bJB.png)


# Installation (There are two methods, with HACS or manual)

### 1. Easy Mode

We support [HACS](https://hacs.netlify.com/). Go to "STORE", search "SamsungTV Custom" and install.

### 2. Manual

Install it as you would do with any homeassistant custom component:

1. Download `custom_components` folder.
2. Copy the `samsungtv_custom` direcotry within the `custom_components` directory of your homeassistant installation. The `custom_components` directory resides within your homeassistant configuration directory.
**Note**: if the custom_components directory does not exist, you need to create it.
After a correct installation, your configuration directory should look like the following.
    ```
    └── ...
    └── configuration.yaml
    └── custom_components
        └── samsungtv_custom
            └── samsungctl_080b
            └── samsungctl_qled
            └── samsungtvws
            └── __init__.py
            └── media_player.py
            └── manifest.json
            └── tv-token.txt
    ```


# Configuration

1. Enable the component by editing the configuration.yaml file (within the config directory as well).
Edit it by adding the following lines:
    ### Example configuration.yaml for default ctl protocol
    ```
    media_player:
      - platform: samsungtv_custom
        host: IP_ADDRESS
        mac: MAC_ADDRESS
        port: (8001 or 8002)
        sourcelist: '{"PlayStation": "KEY_HDMI1", "RaspberryPi": "KEY_HDMI2", "Chromecast": "KEY_HDMI3"}'
    ```
    ### Example configuration.yaml for ws protocol
    ```
    media_player:
      - platform: samsungtv_custom
        host: IP_ADDRESS
        mac: MAC_ADDRESS
        port: (8001 or 8002)
        sourcelist: '{"PlayStation": "KEY_HDMI1"}'
        protocol: ws
    ```
    ### Example configuration.yaml for ctl_beta protocol
    ```
    media_player:
      - platform: samsungtv_custom
        host: IP_ADDRESS
        port: (8001 or 8002)
        mac: MAC_ADDRESS
        sourcelist: '{"RaspberryPi": "KEY_HDMI2", "Chromecast": "KEY_HDMI3"}'
        protocol: ctl_beta
    ```
    ### Example configuration.yaml for ctl_beta protocol for H/J Models
    ```
     media_player:
       - platform: samsungtv_custom
         host: IP_ADDRESS
         port: (8001 or 8002)
         mac: MAC_ADDRESS
         sourcelist: '{"RaspberryPi": "KEY_HDMI2", "Chromecast": "KEY_HDMI3"}'
         protocol: ctl_beta
         token: kdsjfbsdkjbsdkjfskdjf:2
         id: 07270e01-0078-1000-8cd0-c4576e9dxxxxx
    ```
    - The token get be fetched using https://github.com/eclair4151/SmartCrypto. It's the format `<ctx>:<sessionid>`.
    - The id can be fetched via http://IP_ADDRESS:8001/api/v2/
    ### Example configuration.yaml for ctl_qled protocol
    ```
    media_player:
      - platform: samsungtv_custom
        host: IP_ADDRESS
        port: 8002
        mac: MAC_ADDRESS
        sourcelist: '{"PlayStation": "KEY_HDMI1", "RaspberryPi": "KEY_HDMI2", "Chromecast": "KEY_HDMI3"}'
        applist: "YouTube, Apple TV, Plex, Prime Video, Spotify" (only for QLED and similar)
        protocol: ctl_qled
    ```
    **Note**: This is the same as the configuration for the built-in [Samsung Smart TV](https://www.home-assistant.io/integrations/samsungtv/) component, except for the custom variables.

    ### Custom variables

    - **sourcelist:** (json)(Optional) This contains the visible sources in the dropdown list in media player UI.<br>
    Default value: '{"TV": "KEY_TV", "HDMI": "KEY_HDMI"}'<br>

    - **protocol:** (string)(Optional) This determine which communication protocol will be used:<br/>
    Default value: ctl<br>
    Options:<br>
    **ctl**: Default HA protocol.<br>
    **ws**: For 2016+ TVs models.<br>
    **ctl_beta**: Last beta version of samsungctl.<br>
    **ctl_qled**: Only for latest TV QLED models and similar.<br>

    - **applist:** (list)(Optional) List of the apps you want in the source drop down menu (YouTube, Plex, Prime Video, Universal Guide, Netflix, Apple TV, Steam Link, MyCANAL, Spotify, Molotov, SmartThings, e-Manual, Google Play, Gallery, Rakuten TV, RMC Sport, MYTF1 VOD, Blacknut, Facebook Watch, McAfee Security for TV, OCS, Playzer)<br>
    
2. Reboot Home Assistant
3. Congrats! You're all set!

# Usage

### Send Keys
```
service: media_player.play_media
```

```json
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "send_key",
  "media_content_id": "KEY_CODE",
}
```
**Note**: Change "KEY_CODE" by desired key_code.

## Launch application (only for ctl_qled protocol)
You can use the source droplist or service ``media_player.select_source`` to launch one of the applications of your configuration file.

To launch an other application you must use the ``media_player.play_media`` service.
```
service: media_player.play_media
```
```
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "app",
  "media_content_id": "Application name",
}
```
**Compatible applications (case sensitive):** YouTube, Plex, Prime Video, Universal Guide, Netflix, Apple TV, Steam Link, MyCANAL, Spotify, Molotov, SmartThings, e-Manual, Google Play, Gallery, Rakuten TV, RMC Sport, MYTF1 VOD, Blacknut, Facebook Watch, McAfee Security for TV, OCS, Playzer.

## Launch media file (only for ctl_qled protocol)
```
service: media_player.play_media
```
```
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "url",
  "media_content_id": "MEDIA_URL",
}
```

## Script example:
```
tv_channel_down:
  alias: Channel down
  sequence:
  - service: media_player.play_media
    data:
      entity_id: media_player.samsung_tv55
      media_content_id: KEY_CHDOWN
      media_content_type: "send_key"
```

***Key codes***
---------------
The list of accepted keys may vary depending on the TV model, but the following list has some common key codes and their descriptions.

*Power Keys*
____________
Key|Description
---|-----------
KEY_POWEROFF|PowerOFF
KEY_POWERON|PowerOn
KEY_POWER|PowerToggle

*Input Keys*
____________
Key|Description
---|-----------
KEY_SOURCE|Source
KEY_COMPONENT1|Component1
KEY_COMPONENT2|Component2
KEY_AV1|AV1
KEY_AV2|AV2
KEY_AV3|AV3
KEY_SVIDEO1|SVideo1
KEY_SVIDEO2|SVideo2
KEY_SVIDEO3|SVideo3
KEY_HDMI|HDMI
KEY_HDMI1|HDMI1
KEY_HDMI2|HDMI2
KEY_HDMI3|HDMI3
KEY_HDMI4|HDMI4
KEY_FM_RADIO|FMRadio
KEY_DVI|DVI
KEY_DVR|DVR
KEY_TV|TV
KEY_ANTENA|AnalogTV
KEY_DTV|DigitalTV

*Number Keys*
_____________
Key|Description
---|-----------
KEY_1|Key1
KEY_2|Key2
KEY_3|Key3
KEY_4|Key4
KEY_5|Key5
KEY_6|Key6
KEY_7|Key7
KEY_8|Key8
KEY_9|Key9
KEY_0|Key0

*Misc Keys*
___________
Key|Description
---|-----------
KEY_PANNEL_CHDOWN|3D
KEY_ANYNET|AnyNet+
KEY_ESAVING|EnergySaving
KEY_SLEEP|SleepTimer
KEY_DTV_SIGNAL|DTVSignal

*Channel Keys*
______________
Key|Description
---|-----------
KEY_CHUP|ChannelUp
KEY_CHDOWN|ChannelDown
KEY_PRECH|PreviousChannel
KEY_FAVCH|FavoriteChannels
KEY_CH_LIST|ChannelList
KEY_AUTO_PROGRAM|AutoProgram
KEY_MAGIC_CHANNEL|MagicChannel

*Volume Keys*
_____________
Key|Description
---|-----------
KEY_VOLUP|VolumeUp
KEY_VOLDOWN|VolumeDown
KEY_MUTE|Mute

*Direction Keys*
________________
Key|Description
---|-----------
KEY_UP|NavigationUp
KEY_DOWN|NavigationDown
KEY_LEFT|NavigationLeft
KEY_RIGHT|NavigationRight
KEY_RETURN|NavigationReturn/Back
KEY_ENTER|NavigationEnter

*Media Keys*
____________
Key|Description
---|-----------
KEY_REWIND|Rewind
KEY_STOP|Stop
KEY_PLAY|Play
KEY_FF|FastForward
KEY_REC|Record
KEY_PAUSE|Pause
KEY_LIVE|Live
KEY_QUICK_REPLAY|fnKEY_QUICK_REPLAY
KEY_STILL_PICTURE|fnKEY_STILL_PICTURE
KEY_INSTANT_REPLAY|fnKEY_INSTANT_REPLAY

*Picture in Picture*
____________________
Key|Description
---|-----------
KEY_PIP_ONOFF|PIPOn/Off
KEY_PIP_SWAP|PIPSwap
KEY_PIP_SIZE|PIPSize
KEY_PIP_CHUP|PIPChannelUp
KEY_PIP_CHDOWN|PIPChannelDown
KEY_AUTO_ARC_PIP_SMALL|PIPSmall
KEY_AUTO_ARC_PIP_WIDE|PIPWide
KEY_AUTO_ARC_PIP_RIGHT_BOTTOM|PIPBottomRight
KEY_AUTO_ARC_PIP_SOURCE_CHANGE|PIPSourceChange
KEY_PIP_SCAN|PIPScan

*Modes*
_______
Key|Description
---|-----------
KEY_VCR_MODE|VCRMode
KEY_CATV_MODE|CATVMode
KEY_DSS_MODE|DSSMode
KEY_TV_MODE|TVMode
KEY_DVD_MODE|DVDMode
KEY_STB_MODE|STBMode
KEY_PCMODE|PCMode

*Color Keys*
____________
Key|Description
---|-----------
KEY_GREEN|Green
KEY_YELLOW|Yellow
KEY_CYAN|Cyan
KEY_RED|Red

*Teletext*
__________
Key|Description
---|-----------
KEY_TTX_MIX|TeletextMix
KEY_TTX_SUBFACE|TeletextSubface

*AspectRatio*
______________
Key|Description
---|-----------
KEY_ASPECT|AspectRatio
KEY_PICTURE_SIZE|PictureSize
KEY_4_3|AspectRatio4:3
KEY_16_9|AspectRatio16:9
KEY_EXT14|AspectRatio3:4(Alt)
KEY_EXT15|AspectRatio16:9(Alt)

*Picture Mode*
______________
Key|Description
---|-----------
KEY_PMODE|PictureMode
KEY_PANORAMA|PictureModePanorama
KEY_DYNAMIC|PictureModeDynamic
KEY_STANDARD|PictureModeStandard
KEY_MOVIE1|PictureModeMovie
KEY_GAME|PictureModeGame
KEY_CUSTOM|PictureModeCustom
KEY_EXT9|PictureModeMovie(Alt)
KEY_EXT10|PictureModeStandard(Alt)

*Menus*
_______
Key|Description
---|-----------
KEY_MENU|Menu
KEY_TOPMENU|TopMenu
KEY_TOOLS|Tools
KEY_HOME|Home
KEY_CONTENTS|Contents
KEY_GUIDE|Guide
KEY_DISC_MENU|DiscMenu
KEY_DVR_MENU|DVRMenu
KEY_HELP|Help

*OSD*
_____
Key|Description
---|-----------
KEY_INFO|Info
KEY_CAPTION|Caption
KEY_CLOCK_DISPLAY|ClockDisplay
KEY_SETUP_CLOCK_TIMER|SetupClock
KEY_SUB_TITLE|Subtitle

*Zoom*
______
Key|Description
---|-----------
KEY_ZOOM_MOVE|ZoomMove
KEY_ZOOM_IN|ZoomIn
KEY_ZOOM_OUT|ZoomOut
KEY_ZOOM1|Zoom1
KEY_ZOOM2|Zoom2

*Other Keys*
____________
Key|Description
---|-----------
KEY_WHEEL_LEFT|WheelLeft
KEY_WHEEL_RIGHT|WheelRight
KEY_ADDDEL|Add/Del
KEY_PLUS100|Plus100
KEY_AD|AD
KEY_LINK|Link
KEY_TURBO|Turbo
KEY_CONVERGENCE|Convergence
KEY_DEVICE_CONNECT|DeviceConnect
KEY_11|Key11
KEY_12|Key12
KEY_FACTORY|KeyFactory
KEY_3SPEED|Key3SPEED
KEY_RSURF|KeyRSURF
KEY_FF_|FF_
KEY_REWIND_|REWIND_
KEY_ANGLE|Angle
KEY_RESERVED1|Reserved1
KEY_PROGRAM|Program
KEY_BOOKMARK|Bookmark
KEY_PRINT|Print
KEY_CLEAR|Clear
KEY_VCHIP|VChip
KEY_REPEAT|Repeat
KEY_DOOR|Door
KEY_OPEN|Open
KEY_DMA|DMA
KEY_MTS|MTS
KEY_DNIe|DNIe
KEY_SRS|SRS
KEY_CONVERT_AUDIO_MAINSUB|ConvertAudioMain/Sub
KEY_MDC|MDC
KEY_SEFFECT|SoundEffect
KEY_PERPECT_FOCUS|PERPECTFocus
KEY_CALLER_ID|CallerID
KEY_SCALE|Scale
KEY_MAGIC_BRIGHT|MagicBright
KEY_W_LINK|WLink
KEY_DTV_LINK|DTVLink
KEY_APP_LIST|ApplicationList
KEY_BACK_MHP|BackMHP
KEY_ALT_MHP|AlternateMHP
KEY_DNSe|DNSe
KEY_RSS|RSS
KEY_ENTERTAINMENT|Entertainment
KEY_ID_INPUT|IDInput
KEY_ID_SETUP|IDSetup
KEY_ANYVIEW|AnyView
KEY_MS|MS
KEY_MORE|
KEY_MIC|
KEY_NINE_SEPERATE|
KEY_AUTO_FORMAT|AutoFormat
KEY_DNET|DNET

*Auto Arc Keys*
_______________
Key|Description
---|-----------
KEY_AUTO_ARC_C_FORCE_AGING|
KEY_AUTO_ARC_CAPTION_ENG|
KEY_AUTO_ARC_USBJACK_INSPECT|
KEY_AUTO_ARC_RESET|
KEY_AUTO_ARC_LNA_ON|
KEY_AUTO_ARC_LNA_OFF|
KEY_AUTO_ARC_ANYNET_MODE_OK|
KEY_AUTO_ARC_ANYNET_AUTO_START|
KEY_AUTO_ARC_CAPTION_ON|
KEY_AUTO_ARC_CAPTION_OFF|
KEY_AUTO_ARC_PIP_DOUBLE|
KEY_AUTO_ARC_PIP_LARGE|
KEY_AUTO_ARC_PIP_LEFT_TOP|
KEY_AUTO_ARC_PIP_RIGHT_TOP|
KEY_AUTO_ARC_PIP_LEFT_BOTTOM|
KEY_AUTO_ARC_PIP_CH_CHANGE|
KEY_AUTO_ARC_AUTOCOLOR_SUCCESS|
KEY_AUTO_ARC_AUTOCOLOR_FAIL|
KEY_AUTO_ARC_JACK_IDENT|
KEY_AUTO_ARC_CAPTION_KOR|
KEY_AUTO_ARC_ANTENNA_AIR|
KEY_AUTO_ARC_ANTENNA_CABLE|
KEY_AUTO_ARC_ANTENNA_SATELLITE|

*Panel Keys*
____________
Key|Description
---|-----------
KEY_PANNEL_POWER|
KEY_PANNEL_CHUP|
KEY_PANNEL_VOLUP|
KEY_PANNEL_VOLDOW|
KEY_PANNEL_ENTER|
KEY_PANNEL_MENU|
KEY_PANNEL_SOURCE|
KEY_PANNEL_ENTER|

<br></br>
*Extended Keys*
_______________
Key|Description
---|-----------
KEY_EXT1|
KEY_EXT2|
KEY_EXT3|
KEY_EXT4|
KEY_EXT5|
KEY_EXT6|
KEY_EXT7|
KEY_EXT8|
KEY_EXT11|
KEY_EXT12|
KEY_EXT13|
KEY_EXT16|
KEY_EXT17|
KEY_EXT18|
KEY_EXT19|
KEY_EXT20|
KEY_EXT21|
KEY_EXT22|
KEY_EXT23|
KEY_EXT24|
KEY_EXT25|
KEY_EXT26|
KEY_EXT27|
KEY_EXT28|
KEY_EXT29|
KEY_EXT30|
KEY_EXT31|
KEY_EXT32|
KEY_EXT33|
KEY_EXT34|
KEY_EXT35|
KEY_EXT36|
KEY_EXT37|
KEY_EXT38|
KEY_EXT39|
KEY_EXT40|
KEY_EXT41|

Please note that some codes are different on the 2016+ TVs. For example, `KEY_POWEROFF` is `KEY_POWER` on the newer TVs.

***References***
----------------

The code list has been extracted from: https://github.com/kdschlosser/samsungctl<br>
ws wrapper protocol from: https://github.com/xchwarze/samsung-tv-ws-api<br>
Qled integration from: https://github.com/giefca/ha-samsungtv-qled
