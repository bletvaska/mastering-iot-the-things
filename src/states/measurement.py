from time import sleep

from .connect_network import ConnectNetwork
from hw.mixins.temperature import TemperatureUnit
from .base import BaseState


class Measurement(BaseState):
    name = "Measurement"

    def exec(self):
        value = self.context.temperature_sensor.temperature(unit=TemperatureUnit.METRIC)
        print(f'Current Temperature is {value}')

        sleep(1)

        value = self.context.humidity_sensor.humidity()
        print(f'Current Humidity is {value}')

        return ConnectNetwork(self.context)
