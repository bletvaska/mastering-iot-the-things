from time import sleep
from machine import reset, soft_reset
from .base import BaseCommand


class Reset(BaseCommand):
    name = 'reset'
    description = 'Soft/Hard reset'
    usage = (
        ('reset soft', 'Soft reset.'),
        ('reset hard', 'Hard reset.'),
    )

    def __call__(self, params: list) -> None:
        if len(params) != 1 or params[0] not in ['soft', 'hard']:
            print('Wrong usage.')
            print(self)
            return

        if params[0] == 'soft':
            print('Soft reset.')
            sleep(0.1)
            soft_reset()

        elif params[0] == 'hard':
            print('Hard reset.')
            sleep(0.1)
            reset()
