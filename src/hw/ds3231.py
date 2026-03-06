from hw.mixins.actuators.alarm import AlarmMixin
from hw.mixins.sensors.clock import ClockMixin


class DS3231(ClockMixin, AlarmMixin):
    pass
