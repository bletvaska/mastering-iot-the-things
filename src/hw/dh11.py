from machine import Pin
import dht

from hw.mixins.sensors.humidity import HumidityMixin
from hw.mixins.sensors.temperature import TemperatureMixin, TemperatureUnit


class DHT11(TemperatureMixin, HumidityMixin):
    def __init__(self, pinnr):
        pin = Pin(pinnr, Pin.IN)
        self.sensor = dht.DHT11(pin)

    def temperature(self, unit=TemperatureUnit.STANDARD) -> float:
        self.sensor.measure()
        value = self.sensor.temperature()

        if unit == TemperatureUnit.IMPERIAL:
            return (value * 9 / 5) + 32
        elif unit == TemperatureUnit.STANDARD:
            return value - 273
        elif unit == TemperatureUnit.METRIC:
            return value

        raise ValueError(f'Invalid temperature unit: {unit}')

    def humidity(self) -> int:
        self.sensor.measure()
        return self.sensor.humidity()
