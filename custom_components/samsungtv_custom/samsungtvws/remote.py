import base64
import json
import logging
import time
import ssl
import websocket


class SamsungTVWS():
    _URL_FORMAT = 'wss://{host}:{port}/api/v2/channels/samsung.remote.control?name={name}'
    _SSL_URL_FORMAT = 'wss://{host}:{port}/api/v2/channels/samsung.remote.control?name={name}&token={token}'

    def __init__(self, host, token=None, token_file=None, port=8002, timeout=None, key_press_delay=1.5, name='SamsungTvRemote'):
        self.host = host
        self.token = token
        self.token_file = token_file
        self.port = port
        self.timeout = None if timeout == 0 else timeout
        self.key_press_delay = key_press_delay
        self.name = name
        self.connection = None

    def __exit__(self, type, value, traceback):
        self.close()

    def _serialize_string(self, string):
        if isinstance(string, str):
            string = str.encode(string)

        return base64.b64encode(string).decode('utf-8')

    def _is_ssl_connection(self):
        return self.token is not None or \
               self.token_file is not None or \
               self.port == 8002

    def _format_websocket_url(self, is_ssl=False):
        params = {
            'host': self.host,
            'port': self.port,
            'name': self._serialize_string(self.name),
            'token': self._get_token(),
        }

        if is_ssl:
            return self._SSL_URL_FORMAT.format(**params)
        else:
            return self._URL_FORMAT.format(**params)

    def _get_token(self):
        if self.token_file is not None:
            with open(self.token_file, 'r') as token_file:
                return token_file.readline()
        else:
            return self.token

    def _set_token(self, token):
        if self.token_file is not None:
            with open(self.token_file, 'w') as token_file:
                token_file.write(token)
        else:
            logging.info('New token %s', token)

    def _ws_send(self, payload):
        if self.connection is None:
            self.open()

        self.connection.send(payload)
        time.sleep(self.key_press_delay)

    def open(self):
        is_ssl = self._is_ssl_connection()
        url = self._format_websocket_url(is_ssl)
        sslopt = {'cert_reqs': ssl.CERT_NONE} if is_ssl else {}

        logging.debug('WS url %s', url)

        self.connection = websocket.create_connection(
            url,
            self.timeout,
            sslopt=sslopt
        )

        response = json.loads(self.connection.recv())

        if response.get('data') and response.get('data').get('token'):
            token = response.get('data').get('token')
            self._set_token(token)

        if response['event'] != 'ms.channel.connect':
            self.close()
            raise Exception(response)

    def close(self):
        if self.connection:
            self.connection.close()

        self.connection = None
        logging.debug('Connection closed.')

    def send_key(self, key):
        payload = json.dumps({
            'method': 'ms.remote.control',
            'params': {
                'Cmd': 'Click',
                'DataOfCmd': key,
                'Option': 'false',
                'TypeOfRemote': 'SendRemoteKey'
            }
        })

        logging.info('Sending key %s', key)
        self._ws_send(payload)

    def open_browser(self, url):
        payload = json.dumps({
            'method': 'ms.channel.emit',
            'params': {
                'event': 'ed.apps.launch',
                'to': 'host',
                'data': {
                    'appId': 'org.tizen.browser',
                    'action_type': 'NATIVE_LAUNCH',
                    'metaTag': url
                }
            }
        })

        logging.info('Opening url in browser %s', url)
        self._ws_send(payload)

    def run_app(self, app_id):
        payload = json.dumps({
            'method': 'ms.channel.emit',
            'params': {
                'event': 'ed.apps.launch',
                'to': 'host',
                'data': {
                    'action_type': 'NATIVE_LAUNCH', # or 'DEEP_LINK'
                    'appId': app_id
                }
            }
        })

        logging.info('Sending run_app %s', app_id)
        self._ws_send(payload)

    def app_list(self):
        # TODO incomplete function!
        payload = json.dumps({
            'method': 'ms.channel.emit',
            'params': {
                'event': 'ed.installedApp.get',
                'to': 'host'
            }
        })

        self._ws_send(payload)

    # power
    def power(self):
        self.send_key('KEY_POWER')

    # menu
    def home(self):
        self.send_key('KEY_HOME')

    def menu(self):
        self.send_key('KEY_MENU')

    def source(self):
        self.send_key('KEY_SOURCE')

    def guide(self):
        self.send_key('KEY_GUIDE')

    def tools(self):
        self.send_key('KEY_TOOLS')

    def info(self):
        self.send_key('KEY_INFO')

    # navigation
    def up(self):
        self.send_key('KEY_UP')

    def down(self):
        self.send_key('KEY_DOWN')

    def left(self):
        self.send_key('KEY_LEFT')

    def right(self):
        self.send_key('KEY_RIGHT')

    def enter(self, count=1):
        self.send_key('KEY_ENTER')

    def back(self):
        self.send_key('KEY_RETURN')

    # channel
    def channel_list(self):
        self.send_key('KEY_CH_LIST')

    def channel(self, ch):
        for c in str(ch):
            self.digit(c)
        self.enter()

    def digit(self, d):
        self.send_key('KEY_' + d)

    def channel_up(self):
        self.send_key('KEY_CHUP')

    def channel_down(self):
        self.send_key('KEY_CHDOWN')

    # volume
    def volume_up(self):
        self.send_key('KEY_VOLUP')

    def volume_down(self):
        self.send_key('KEY_VOLDOWN')

    def mute(self):
        self.send_key('KEY_MUTE')

    # extra
    def red(self):
        self.send_key('KEY_RED')

    def green(self):
        self.send_key('KEY_GREEN')

    def yellow(self):
        self.send_key('KEY_YELLOW')

    def blue(self):
        self.send_key('KEY_BLUE')
