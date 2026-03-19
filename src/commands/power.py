from .base import BaseCommand
from constants import ALIAS_POWER


class Power(BaseCommand):
    name = 'power'
    description = 'Power management information.'
    usage = (
        ('power stat', 'Show current power status.'),
    )

    def __call__(self, params: list) -> None:
        if len(params) == 0:
            print(self)
            return

        dispatch = {
            'stat': self._stat,
        }

        handler = dispatch.get(params[0])
        if handler:
            handler(params[1:])
        else:
            print('Error: Wrong Usage')
            print(self)

    def _stat(self, params):
        monitor = self.context.devices.get(ALIAS_POWER)

        print(f"{'Source':<10}: {monitor.power_source()}")
        print(f"{'Voltage':<10}: {monitor.battery_voltage():.2f} V")
        print(f"{'Charge':<10}: {monitor.battery_percent():.1f} %")
