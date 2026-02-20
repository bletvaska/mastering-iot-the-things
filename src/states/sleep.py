from time import sleep

from .base import BaseState


class Sleep(BaseState):
    name = "Sleep"

    def exec(self):
        self.context.diag_led[0] = (0, 0, 0)
        self.context.diag_led.write()

        sleep(1)  # aby vsetci stihli spravit to, co treba
        # deepsleep()
        return None
