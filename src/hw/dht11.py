import time
from machine import Pin
import dht

from hw.base import BaseDevice
from hw.mixins.sensors.humidity import HumidityMixin
from hw.mixins.sensors.temperature import TemperatureMixin, TemperatureUnit


class DHT11(TemperatureMixin, HumidityMixin, BaseDevice):
    name = 'DHT11'
    description = 'Temperature and humidity sensor'

    def __init__(self, pin: int, alias=None):
        BaseDevice.__init__(self, alias)
        self.pins = {'data': pin}
        pin = Pin(pin, Pin.IN)
        self.sensor = dht.DHT11(pin)
        self._last_measurement = None

    def _measure(self):
        if self._last_measurement is None or time.ticks_diff(time.ticks_ms(), self._last_measurement) >= 1000:
            self.sensor.measure()
            self._last_measurement = time.ticks_ms()
            print(self._last_measurement)


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
