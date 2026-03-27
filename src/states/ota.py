import json

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
        print('handling settings')

    def _handle_cmd(self, topic: str, message: dict):
        print('handling command')
