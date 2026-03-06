from umqtt.simple import MQTTClient

from .publish import Publish
from .base import BaseState
from helpers import do_connect


class ConnectNetwork(BaseState):
    def exec(self):
        settings = self.context.settings

        # connect to wifi
        wifi = settings.wifi
        do_connect(wifi.ssid, wifi.password)

        # connect to mqtt
        mqtt = settings.mqtt
        device_id = settings.device_id
        self.context.mqtt_client = MQTTClient(
            device_id,
            mqtt.broker,
            port=mqtt.port,
            user=mqtt.username,
            password=mqtt.password,
            keepalive=10,
            ssl=not mqtt.insecure
        )

        self.context.mqtt_client.set_last_will(
            f'{settings.base_topic()}/status',
            '{"status": "offline", "owner": "mirek", "reason": "lastwill"}',
            retain=True
        )

        self.context.mqtt_client.connect()

        self.context.mqtt_client.publish(
            f'{settings.base_topic()}/status',
            '{"status": "online", "owner": "mirek"}',
            retain=True
        )

        # self.context.mqtt_client.ping()

        return Publish(self.context)
