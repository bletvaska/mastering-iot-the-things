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

    def exec(self) -> None:
        if len(self.params) != 1 or self.params[0] not in ['soft', 'hard']:
            print('Wrong usage.')
            self.show_usage()
            return

        if self.params[0] == 'soft':
            print('Soft reset.')
            sleep(0.1)
            soft_reset()

        if self.params[0] == 'hard':
            print('Hard reset.')
            sleep(0.1)
            reset()
