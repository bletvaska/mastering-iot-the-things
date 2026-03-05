from time import sleep

from machine import reset

from commands.base import BaseCommand

class Reset(BaseCommand):
    name = 'reset'
    description = 'Soft/Hard reset'

    def exec(self) -> None:
        print('Going to reset')
        sleep(0.1)
        reset()
