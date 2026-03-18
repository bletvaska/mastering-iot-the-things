import ntptime

from umqtt.simple import MQTTClient

from constants import SALT_FILE, ALIAS_WIFI
from crypto import decrypt
from .publish import Publish
from .base import BaseState


class ConnectNetwork(BaseState):
    name = "Connect Network"

    def exec(self):
        settings = self.context.settings

        # connect to wifi
        wifi = settings.wifi
        self.context.devices.get(ALIAS_WIFI).connect(wifi.ssid, decrypt(wifi.password, SALT_FILE))
        ntptime.settime()

        # connect to mqtt
        mqtt = settings.mqtt
        device_id = settings.device_id
        self.context.mqtt_client = MQTTClient(
            device_id,
            mqtt.broker,
            port=mqtt.port,
            user=mqtt.username,
            password=decrypt(mqtt.password, SALT_FILE),
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
