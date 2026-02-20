from time import sleep

from hw.mixins.temperature import TemperatureMixin
from .sleep import Sleep
from .base import BaseState


class Measurement(BaseState):
    name = "Measurement"

    def exec(self):
        value = self.context.temperature_sensor.temperature(unit=TemperatureMixin.Unit.METRIC)
        print(f'Current Temperature is {value}')

        sleep(1)

        value = self.context.humidity_sensor.humidity()
        print(f'Current Humidity is {value}')

        return Sleep(self.context)
