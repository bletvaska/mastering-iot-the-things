from .sleep import Sleep
from .base import BaseState


class Publish(BaseState):
    name = "Publish"

    def exec(self):
        return Sleep(self.context)
