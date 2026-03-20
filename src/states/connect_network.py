import ntptime
from machine import RTC

from umqtt.simple import MQTTClient

from constants import SALT_FILE, ALIAS_WIFI, ALIAS_RTC
from crypto import decrypt
from .publish import Publish
from .base import BaseState


class ConnectNetwork(BaseState):
    name = "Connect Network"

    def exec(self):
        settings = self.context.settings

        # connect to wifi
        wifi = self.context.devices.get(ALIAS_WIFI)
        wifi.connect(settings.wifi.ssid, decrypt(settings.wifi.password, SALT_FILE))

        # sync time
        ntptime.settime()
        rtc = self.context.devices.get(ALIAS_RTC)
        rtc.datetime(RTC().datetime())

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
