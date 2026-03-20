import time
from machine import Pin
from dht import DHT22 as DHT

from hw.base import BaseDevice
from hw.mixins.sensors.humidity import HumidityMixin
from hw.mixins.sensors.temperature import TemperatureMixin, TemperatureUnit

_MEASUREMENT_INTERVAL_MS = 3000


class DHT22(TemperatureMixin, HumidityMixin, BaseDevice):
    name = 'DHT22'
    description = 'Temperature and humidity sensor'

    def __init__(self, pin: int, alias=None):
        BaseDevice.__init__(self, alias)
        self.pins = {'data': pin}
        pin = Pin(pin, Pin.IN)
        self.sensor = DHT(pin)
        self._last_measurement = None

    def _measure(self):
        if self._last_measurement is None or time.ticks_diff(time.ticks_ms(),
                                                             self._last_measurement) >= _MEASUREMENT_INTERVAL_MS:
            self.sensor.measure()
            self._last_measurement = time.ticks_ms()

    def temperature(self, unit=TemperatureUnit.METRIC) -> float:
        self._measure()
        value = self.sensor.temperature()

        if unit == TemperatureUnit.IMPERIAL:
            return (value * 9 / 5) + 32
        elif unit == TemperatureUnit.STANDARD:
            return value + 273.15
        elif unit == TemperatureUnit.METRIC:
            return value

        raise ValueError(f'Invalid temperature unit: {unit}')

    def humidity(self) -> int:
        self._measure()
        return self.sensor.humidity()
