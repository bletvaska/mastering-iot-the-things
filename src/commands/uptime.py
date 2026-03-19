from time import ticks_ms, ticks_diff

from .base import BaseCommand


class Uptime(BaseCommand):
    name = 'uptime'
    description = 'Show time elapsed since last restart.'

    def __call__(self, params: list) -> None:
        elapsed_ms = ticks_diff(ticks_ms(), self.context.started_at)
        elapsed_s = elapsed_ms // 1000

        days    = elapsed_s // 86400
        hours   = (elapsed_s % 86400) // 3600
        minutes = (elapsed_s % 3600) // 60
        seconds = elapsed_s % 60

        print(f'Uptime: {days}d {hours:02}:{minutes:02}:{seconds:02}')
