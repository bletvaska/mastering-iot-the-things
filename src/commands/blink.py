from time import sleep

from commands.base import BaseCommand


class Blink(BaseCommand):
    name = 'blink'
    description = 'Blinks the diagnostic LED'

    def exec(self) -> None:
        self.context.diag_led.toggle()
        sleep(2)
        self.context.diag_led.toggle()

