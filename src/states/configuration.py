import binascii
import json
import machine
from time import sleep

from constants import SETTINGS_FILE
from models.settings import Settings
from .base import BaseState


class Configuration(BaseState):
    name = "Configuration"
    def enter(self) -> None:
        super().enter()

        self.context.diag_led.set_color(255, 165, 0)

    def exec(self):
        print('>> Creating default settings.')

        # create default settings
        settings = Settings()
        settings.wifi.ssid = 'hello.world'
        settings.wifi.password = 'jahodka123'

        uid = machine.unique_id()
        settings.device_id = binascii.hexlify(uid).decode()
        settings.name = 'THSensor'

        # mqtt configuration
        settings.mqtt.broker = 'greenhub.fei.tuke.sk'
        settings.mqtt.port = 8883
        settings.mqtt.username = 'riesitel'
        settings.mqtt.password = '2VN1zAW0zyffPv'
        settings.mqtt.insecure = False
        settings.mqtt.topic_prefix = 'sub/sk/za/thsensor/'

        # save default settings to file
        data = settings.model_dump()
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(data, file)

        # reset
        sleep(5)
        machine.reset()
