from time import sleep

from .base import BaseState


class Sleep(BaseState):
    name = "Sleep"

    def exec(self):
        self.context.diag_led.off()

        sleep(1)  # aby vsetci stihli spravit to, co treba
        # deepsleep()
        return None
