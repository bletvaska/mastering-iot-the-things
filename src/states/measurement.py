from .sleep import Sleep
from .base import BaseState


class Measurement(BaseState):
    name = "Measurement"

    def exec(self):
        return Sleep(self.context)
