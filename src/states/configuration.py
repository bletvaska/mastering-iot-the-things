import binascii
import json
import pathlib
import machine
from time import sleep

from constants import SETTINGS_FILE, SALT_FILE, DATA_FOLDER
from crypto import create_salt, encrypt
from models.settings import Settings
from .base import BaseState


class Configuration(BaseState):
    name = "Configuration"
    def enter(self) -> None:
        from hw.ws2812b import WS2812B
        self.context.devices.get(WS2812B).set_color(255, 165, 0)

    def exec(self):
        print('>> Creating default settings.')

        # create salt
        create_salt(SALT_FILE)

        # create default settings
        settings = Settings()
        settings.wifi.ssid = 'hello.world'
        settings.wifi.password = encrypt('jahodka123', SALT_FILE)

        uid = machine.unique_id()
        settings.device_id = binascii.hexlify(uid).decode()
        settings.name = 'THSensor'

        # mqtt configuration
        settings.mqtt.broker = 'greenhub.fei.tuke.sk'
        settings.mqtt.port = 8883
        settings.mqtt.username = 'riesitel'
        settings.mqtt.password = encrypt('2VN1zAW0zyffPv', SALT_FILE)
        settings.mqtt.insecure = False
        settings.mqtt.topic_prefix = 'sub/sk/za/thsensor'

        # save default settings to file
        pathlib.Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)
        data = settings.model_dump()
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(data, file)

        # reset
        sleep(5)
        machine.reset()
