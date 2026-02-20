from .measurement import Measurement
from .base import BaseState


class Init(BaseState):
    name = "Init"

    def exec(self):
        return Measurement(self.context)
