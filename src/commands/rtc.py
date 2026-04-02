import ntptime

from .base import BaseCommand
from constants import ALIAS_RTC
from helpers import to_iso8601


class RTC(BaseCommand):
    name = 'rtc'
    description = 'Real-time clock management.'
    usage = (
        ('rtc show', 'Show current date and time.'),
        ('rtc set <YYYY-MM-DDTHH:MM:SS>', 'Set date and time.'),
        ('rtc sync', 'Synchronize time from NTP.'),
    )

    def __call__(self, params: list) -> None:
        if len(params) == 0:
            print(self)
            return

        dispatch = {
            'show': self._show,
            'set':  self._set,
            'sync': self._sync,
        }

        handler = dispatch.get(params[0])
        if handler:
            handler(params[1:])
        else:
            print('Error: Wrong Usage')
            print(self)

    def _show(self, params):
        rtc = self.context.devices.get(ALIAS_RTC)
        print(to_iso8601(rtc.datetime()))

    def _set(self, params):
        if len(params) != 1:
            print('Error: Wrong Usage')
            print(self)
            return

        try:
            date, time = params[0].split('T')
            year, month, day = (int(x) for x in date.split('-'))
            hour, minute, second = (int(x) for x in time.split(':'))
        except (ValueError, AttributeError):
            print('Error: Invalid format. Expected YYYY-MM-DDTHH:MM:SS')
            return

        rtc = self.context.devices.get(ALIAS_RTC)
        rtc.datetime((year, month, day, 0, hour, minute, second, 0))
        print(to_iso8601(rtc.datetime()))

    def _sync(self, params):
        if not self.context.devices.get(ALIAS_RTC):
            print('Error: RTC not available.')
            return

        ntptime.host = self.context.settings.ntp.server
        print(f'NTP server  : {ntptime.host}')

        try:
            ntptime.settime()
        except OSError:
            print('Error: Sync failed. Device is not connected to the internet.')
            return

        import machine
        dt = machine.RTC().datetime()
        rtc = self.context.devices.get(ALIAS_RTC)
        rtc.datetime(dt)
        print(to_iso8601(rtc.datetime()))
