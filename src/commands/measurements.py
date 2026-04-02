from .base import BaseCommand
from constants import METRICS_FILE, ALIAS_RTC, ALIAS_TEMP, ALIAS_HUMIDITY
from helpers import to_iso8601
from hw.mixins.sensors.temperature import TemperatureUnit


class Measurements(BaseCommand):
    name = 'measurements'
    description = 'Manage measurements.'
    usage = (
        ('measurements list',  'Show stored measurements.'),
        ('measurements count', 'Show number of stored measurements.'),
        ('measurements now',   'Take an immediate measurement.'),
        ('measurements clear', 'Delete all stored measurements.'),
    )

    def __call__(self, params: list) -> None:
        if len(params) == 0:
            print(self)
            return

        dispatch = {
            'list':  self._list,
            'count': self._count,
            'now':   self._now,
            'clear': self._clear,
        }

        handler = dispatch.get(params[0])
        if handler:
            handler(params[1:])
        else:
            print('Error: Wrong Usage')
            print(self)

    def _list(self, params):
        try:
            with open(METRICS_FILE, 'r') as f:
                lines = f.readlines()
        except OSError:
            print('No measurements found.')
            return

        if not lines:
            print('No measurements found.')
            return

        print(f'{"Datetime":<22} {"Temperature":>12} {"Unit":<10} {"Humidity":>10}')
        print('-' * 58)
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(';')
            if len(parts) == 4:
                dt, temp, unit, humidity = parts
                print(f'{dt:<22} {temp:>12} {unit:<10} {humidity:>10}')
            else:
                print(line)

    def _count(self, params):
        try:
            with open(METRICS_FILE, 'r') as f:
                count = sum(1 for line in f if line.strip())
            print(f'{count} measurement(s).')
        except OSError:
            print('0 measurements.')

    def _now(self, params):
        rtc = self.context.devices.get(ALIAS_RTC)
        now = rtc.datetime()

        temperature = self.context.devices.get(ALIAS_TEMP).temperature(unit=TemperatureUnit.METRIC)
        humidity = self.context.devices.get(ALIAS_HUMIDITY).humidity()

        with open(METRICS_FILE, 'a') as f:
            print(f'{to_iso8601(now)};{temperature};{TemperatureUnit.METRIC};{humidity}', file=f)

        print(f'Temperature : {temperature} {TemperatureUnit.METRIC}')
        print(f'Humidity    : {humidity}')

    def _clear(self, params):
        try:
            METRICS_FILE.unlink()
            print('Measurements cleared.')
        except OSError:
            print('No measurements to clear.')
