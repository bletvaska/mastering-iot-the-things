from .base import BaseState


class Sleep(BaseState):
    name = "Sleep"

    def exec(self):
        return self

