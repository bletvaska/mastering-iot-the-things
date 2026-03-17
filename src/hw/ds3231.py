from hw.base import BaseDevice
from hw.mixins.actuators.alarm import AlarmMixin
from hw.mixins.sensors.clock import ClockMixin


class DS3231(ClockMixin, AlarmMixin, BaseDevice):
    name = 'DS3231'
    description = 'Real-time clock with alarm'

    def __init__(self, sda, scl, alarm, alias=None):
        BaseDevice.__init__(self, alias)
        self.pins = {'sda': sda, 'scl': scl, 'alarm': alarm}
