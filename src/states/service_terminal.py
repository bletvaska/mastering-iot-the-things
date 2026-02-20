import machine

from .base import BaseState


class ServiceTerminal(BaseState):
    name = "Service Terminal"

    def enter(self) -> None:
        super().enter()

        self.context.diag_led.set_color(5, 5, 5)

    def exec(self):
        # machine.reset()
        return None
