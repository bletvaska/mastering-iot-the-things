from .base import BaseState


class Init(BaseState):
    name = "Init"

    def exec(self):
        return self
