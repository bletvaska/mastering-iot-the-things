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

        self.context.diag_led[0] = (255, 165, 0)
        self.context.diag_led.write()

    def exec(self):
        print('>> Creating default settings.')

        # create default settings
        settings = Settings()
        settings.wifi.ssid = 'hello.world'
        settings.wifi.password = 'jahodka123'

        # save default settings to file
        data = settings.model_dump()
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(data, file)

        # reset
        sleep(5)
        machine.reset()
