import json
from time import ticks_ms

from .factory_reset import FactoryReset
from .configuration import Configuration
from constants import SETTINGS_FILE, SHORT_PRESS_DURATION, LONG_PRESS_DURATION
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
        print(f'ticks: {ticks_ms()}')
        if self.context.btn.value() == 0:

            while self.context.btn.value() == 0:
                if ticks_ms() >= SHORT_PRESS_DURATION:
                    print('>> Short press duration')
                    self.context.diag_led[0] = (255, 165, 0)
                    self.context.diag_led.write()
                    break

            while self.context.btn.value() == 0:
                if ticks_ms() >= LONG_PRESS_DURATION:
                    print('>> Long press duration')
                    self.context.diag_led[0] = (128, 0, 128)
                    self.context.diag_led.write()
                    break

            # wait for btn release
            while self.context.btn.value() == 0:
                pass

            if ticks_ms() >= LONG_PRESS_DURATION:
                return FactoryReset(self.context)

            if ticks_ms() >= SHORT_PRESS_DURATION:
                return Configuration(self.context)

        try:
            # load settings
            with open(SETTINGS_FILE, 'r') as file:
                data = json.load(file)
                self.context.settings = Settings(**data)
        except OSError as ex:
            print('>> Missing settings file.')
            return Configuration(self.context)

        return Measurement(self.context)
