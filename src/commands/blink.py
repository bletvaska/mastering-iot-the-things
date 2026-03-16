from time import sleep

from .base import BaseCommand


class Blink(BaseCommand):
    name = 'blink'
    description = 'Blinks the diagnostic LED'

    def __call__(self, params: list) -> None:
        self.context.diag_led.toggle()
        sleep(2)
        self.context.diag_led.toggle()

