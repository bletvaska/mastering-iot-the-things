import json

from states.configuration import Configuration

from constants import SETTINGS_FILE
from models.settings import Settings

from .measurement import Measurement
from .base import BaseState


class Init(BaseState):
    name = "Init"

    def enter(self) -> None:
        super().enter()

        self.context.diag_led[0] = (0, 255, 0)
        self.context.diag_led.write()

    def exec(self):
        try:
            # load settings
            with open(SETTINGS_FILE, 'r') as file:
                data = json.load(file)
                self.context.settings = Settings(**data)
        except OSError as ex:
            print('>> Missing settings file.')
            return Configuration(self.context)

        return Measurement(self.context)

