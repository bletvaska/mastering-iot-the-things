from time import ticks_ms

from .service_terminal import ServiceTerminal
from .factory_reset import FactoryReset
from .configuration import Configuration
from .measurement import Measurement
from .base import BaseState
from hw.ws2812b import WS2812B
from constants import SETTINGS_FILE, SHORT_PRESS_DURATION, LONG_PRESS_DURATION
from helpers import get_settings


class Init(BaseState):
    name = "Init"

    def enter(self) -> None:
        self.context.devices.get(WS2812B).set_color(0, 255, 0)

        # load settings
        try:
            self.context.settings = get_settings()
        except OSError:
            print('>> Missing settings file.')

    def exec(self):
        if self.context.terminal.value() == 0:
            return ServiceTerminal(self.context)

        if self.context.btn.value() == 0:

            while self.context.btn.value() == 0:
                if ticks_ms() >= SHORT_PRESS_DURATION:
                    print('>> Short press duration')
                    self.context.devices.get(WS2812B).set_color(255, 165, 0)
                    break

            while self.context.btn.value() == 0:
                if ticks_ms() >= LONG_PRESS_DURATION:
                    print('>> Long press duration')
                    self.context.devices.get(WS2812B).set_color(128, 0, 128)
                    break

            # wait for btn release
            while self.context.btn.value() == 0:
                pass

            if ticks_ms() >= LONG_PRESS_DURATION:
                return FactoryReset(self.context)

            if ticks_ms() >= SHORT_PRESS_DURATION:
                return Configuration(self.context)

        if self.context.settings is None:
            return Configuration(self.context)

        return Measurement(self.context)
