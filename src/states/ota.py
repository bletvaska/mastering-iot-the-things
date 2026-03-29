import json

from commands.blink import Blink
from constants import SETTINGS_FILE, SALT_FILE
from crypto import encrypt
from parser import Parser
from .sleep import Sleep
from .base import BaseState


class OTA(BaseState):
    name = "OTA"

    def enter(self) -> None:
        settings = self.context.settings

        self.context.mqtt_client.set_callback(self._on_message)
        self.context.mqtt_client.subscribe(f'{settings.base_topic()}/cmd')
        self.context.mqtt_client.subscribe(f'{settings.base_topic()}/settings')

    def exec(self):
        self.context.mqtt_client.check_msg()
        return Sleep(self.context)

    def exit(self) -> None:
        settings = self.context.settings

        self.context.mqtt_client.unsubscribe(f'{settings.base_topic()}/cmd')
        self.context.mqtt_client.unsubscribe(f'{settings.base_topic()}/settings')

    def _on_message(self, topic: bytes, message: bytes):
        topic = topic.decode('utf-8')
        # print(f'>> Processing message: {message}')
        message = json.loads(message)
        print(f'>>> {topic}: {message}')

        if topic.endswith('/cmd'):
            self._handle_cmd(topic, message)
        elif topic.endswith('/settings'):
            self._handle_settings(topic, message)

    def _handle_settings(self, topic: str, message: dict):
        if 'key' not in message or 'value' not in message:
            print('Error: missing "key" or "value"')
            return

        path = message['key']
        value = message['value']
        keys = path.split('.')

        obj = self.context.settings
        for key in keys[:-1]:
            if not hasattr(obj, key):
                print(f'Error: key "{path}" not found')
                return
            obj = getattr(obj, key)

        last_key = keys[-1]
        if not hasattr(obj, last_key):
            print(f'Error: key "{path}" not found')
            return

        current = getattr(obj, last_key)

        if not isinstance(current, (str, int, float, bool, type(None))):
            print(f'Error: "{path}" is a section, not a value')
            return

        if last_key == 'password':
            value = encrypt(str(value), SALT_FILE)
        elif isinstance(current, bool):
            value = bool(value) if not isinstance(value, bool) else value
        elif isinstance(current, int):
            value = int(value)
        elif isinstance(current, float):
            value = float(value)

        setattr(obj, last_key, value)
        self.context.settings.save(SETTINGS_FILE)
        print(f'Settings updated: {path}')

    def _handle_cmd(self, topic: str, message: dict):
        if 'cmd' not in message:
            print('Error: missing "cmd"')
            return

        parser = Parser()
        parser.register(Blink(self.context))

        result = parser.parse(message['cmd'])
        if result is None:
            print(f'Error: unknown command "{message["cmd"]}"')
            return

        cmd, params = result
        cmd(params)
