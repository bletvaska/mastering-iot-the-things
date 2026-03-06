import json

from .sleep import Sleep
from .base import BaseState


def on_message(topic: bytes, message: bytes):
    topic = topic.decode('utf-8')
    # print(f'>> Processing message: {message}')
    message = json.loads(message)
    print(f'>>> {topic}: {message}')


class OTA(BaseState):
    name = "OTA"

    def enter(self) -> None:
        super().enter()
        settings = self.context.settings

        self.context.mqtt_client.set_callback(on_message)
        self.context.mqtt_client.subscribe(f'{settings.base_topic()}/cmd')
        self.context.mqtt_client.subscribe(f'{settings.base_topic()}/settings')

    def exec(self):
        self.context.mqtt_client.check_msg()
        return Sleep(self.context)

    def exit(self) -> None:
        super().exit()
        settings = self.context.settings

        self.context.mqtt_client.unsubscribe(f'{settings.base_topic()}/cmd')
        self.context.mqtt_client.unsubscribe(f'{settings.base_topic()}/settings')
