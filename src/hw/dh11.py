from machine import Pin
import dht

from hw.mixins.humidity import HumidityMixin
from hw.mixins.temperature import TemperatureMixin


class DHT11(TemperatureMixin, HumidityMixin):
    def __init__(self, pinnr):
        pin = Pin(pinnr, Pin.IN)
        self.sensor = dht.DHT11(pin)

    def temperature(self, unit=TemperatureMixin.Unit.STANDARD) -> float:
        self.sensor.measure()
        value = self.sensor.temperature()

        if unit == TemperatureMixin.Unit.IMPERIAL:
            return (value * 9 / 5) + 32
        elif unit == TemperatureMixin.Unit.STANDARD:
            return value - 273
        elif unit == TemperatureMixin.Unit.METRIC:
            return value

        raise ValueError(f'Invalid temperature unit: {unit}')

    def humidity(self) -> int:
        self.sensor.measure()
        return self.sensor.humidity()
