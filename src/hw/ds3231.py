from machine import I2C, Pin
from lib.ds3231_gen import DS3231 as _DS3231

from hw.base import BaseDevice
from hw.mixins.actuators.alarm import AlarmMixin
from hw.mixins.sensors.clock import ClockMixin


class DS3231(ClockMixin, AlarmMixin, BaseDevice):
    name = 'DS3231'
    description = 'Real-time clock with alarm'

    def __init__(self, sda, scl, alarm, alias=None):
        BaseDevice.__init__(self, alias)
        self.pins = {'sda': sda, 'scl': scl, 'alarm': alarm}
        self._i2c = I2C(0, sda=Pin(sda), scl=Pin(scl))
        self._rtc = _DS3231(self._i2c)
        self._alarm_pin = Pin(alarm, Pin.IN, Pin.PULL_UP)

    def datetime(self, dt=None):
        if dt is None:
            year, month, day, hour, minute, sec, dow, _ = self._rtc.get_time()
            return year, month, day, dow, hour, minute, sec, 0

        year, month, day, dow, hour, minute, sec, _ = dt
        self._rtc.set_time((year, month, day, hour, minute, sec, dow, 0))

    def set_alarm(
            self,
            when: str,
            day: int | None = None,
            hour: int | None = None,
            minute: int | None = None,
            second: int | None = None,
            alarm_id: int = 0,
    ) -> None:

        raise NotImplementedError

    def clear_alarm(self, nr: int = 0):
        if nr == 0:
            self._rtc.alarm1.clear()
        elif nr == 1:
            self._rtc.alarm2.clear()
        else:
            raise ValueError(f'Invalid alarm number {nr}.')
