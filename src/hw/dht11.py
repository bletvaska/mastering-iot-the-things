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

    def temperature(self, units=TemperatureUnit.METRIC) -> float:
        self.sensor.measure()
        value = self.sensor.temperature()

        if units == TemperatureUnit.IMPERIAL:
            return (value * 9 / 5) + 32
        elif units == TemperatureUnit.STANDARD:
            return value + 273.15
        elif units == TemperatureUnit.METRIC:
            return value

        raise ValueError(f'Invalid temperature unit: {units}')

    def humidity(self) -> int:
        self.sensor.measure()
        return self.sensor.humidity()
