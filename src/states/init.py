from .measurement import Measurement
from .base import BaseState


class Init(BaseState):
    name = "Init"

    def enter(self) -> None:
        super().enter()

        self.context.diag_led[0] = (0, 255, 0)
        self.context.diag_led.write()

    def exec(self):
        return Measurement(self.context)
