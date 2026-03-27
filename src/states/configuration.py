import binascii
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
        self.context.devices.get(WS2812B).color((255, 165, 0))

    def exec(self):
        print('>> Creating default settings.')

        # create data folder if doesnt exist
        DATA_FOLDER.mkdir(parents=True, exist_ok=True)

        # create salt
        create_salt(SALT_FILE)

        # create default settings
        settings = Settings()

        settings.wifi.ssid = 'hello.world'
        settings.wifi.password = encrypt('jahodka123', SALT_FILE)

        # uid = machine.unique_id()
        # settings.device_id = binascii.hexlify(uid).decode()
        settings.device_id = 'mirek'
        settings.name = 'THSensor'

        # mqtt configuration
        settings.mqtt.broker = 'greenhub.fei.tuke.sk'
        settings.mqtt.port = 8883
        settings.mqtt.username = 'riesitel'
        settings.mqtt.password = encrypt('2VN1zAW0zyffPv', SALT_FILE)
        settings.mqtt.insecure = False
        settings.mqtt.topic_prefix = 'sub/sk/za/thsensor'

        # user admin
        settings.admin.username = 'admin'
        settings.admin.password = encrypt('admin', SALT_FILE)

        # save default settings to file
        pathlib.Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)
        settings.save(SETTINGS_FILE)


        # # create AP mode
        # ap = network.WLAN(network.AP_IF)
        # ap.config(ssid=SENSOR_SSID, key=SENSOR_WIFI_PASSWORD)
        # ap.active(True)
        # print(ap.ifconfig())
        #
        # # start the web app
        # from web.routes import app
        # app.run(port=80)


        # reset
        sleep(5)
        machine.reset()
