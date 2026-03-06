import json
from time import sleep

from umqtt.simple import MQTTClient

from .sleep import Sleep
from .base import BaseState
from helpers import do_connect


def on_message(topic: bytes, message: bytes):
    topic = topic.decode('utf-8')
    message = json.loads( message )
    print(f'>>> {topic}: {message}')


class ConnectNetwork(BaseState):
    def exec(self):
        settings = self.context.settings

        # connect to wifi
        wifi = settings.wifi
        do_connect(wifi.ssid, wifi.password)

        # connect to mqtt
        mqtt = settings.mqtt
        device_id = settings.device_id
        client = MQTTClient(
            device_id,
            mqtt.broker,
            port=mqtt.port,
            user=mqtt.username,
            password=mqtt.password,
            keepalive=0,
            ssl=not mqtt.insecure
        )
        client.set_callback(on_message)
        client.connect()

        client.publish(f'{settings.base_topic()}/status', 'online')
        client.subscribe(f'{settings.base_topic()}/cmd')

        print('>> Waiting for messages...')
        while True:
            client.check_msg()
            sleep(0.2)

        client.disconnect()

        return Sleep(self.context)



