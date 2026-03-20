from time import ticks_ms, ticks_diff

from .service_terminal import ServiceTerminal
from .factory_reset import FactoryReset
from .configuration import Configuration
from .measurement import Measurement
from .base import BaseState
from hw.ws2812b import WS2812B
from constants import SETTINGS_FILE, SHORT_PRESS_DURATION, LONG_PRESS_DURATION, ALIAS_CONTROL_BTN, ALIAS_SERVICE_BTN
from helpers import get_settings


class Init(BaseState):
    name = "Init"

    def enter(self) -> None:
        self.context.devices.get(WS2812B).color((0, 255, 0))

        # load settings
        try:
            self.context.settings = get_settings()
        except OSError:
            print('>> Missing settings file.')

    def exec(self):
        svc_btn  = self.context.devices.get(ALIAS_SERVICE_BTN)
        ctrl_btn = self.context.devices.get(ALIAS_CONTROL_BTN)

        if svc_btn.is_pressed():
            return ServiceTerminal(self.context)

        if ctrl_btn.is_pressed():

            while ctrl_btn.is_pressed():
                if ticks_diff(ticks_ms(), self.context.started_at) >= SHORT_PRESS_DURATION:
                    print('>> Short press duration')
                    self.context.devices.get(WS2812B).color((255, 165, 0))
                    break

            while ctrl_btn.is_pressed():
                if ticks_diff(ticks_ms(), self.context.started_at) >= LONG_PRESS_DURATION:
                    print('>> Long press duration')
                    self.context.devices.get(WS2812B).color((128, 0, 128))
                    break

            # wait for btn release
            while ctrl_btn.is_pressed():
                pass

            if ticks_diff(ticks_ms(), self.context.started_at) >= LONG_PRESS_DURATION:
                return FactoryReset(self.context)

            if ticks_diff(ticks_ms(), self.context.started_at) >= SHORT_PRESS_DURATION:
                return Configuration(self.context)

        if self.context.settings is None:
            return Configuration(self.context)

        return Measurement(self.context)
