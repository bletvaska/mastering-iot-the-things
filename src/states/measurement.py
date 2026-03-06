from time import sleep

from helpers import to_iso8601
from machine import RTC

from constants import METRICS_FILE
from .connect_network import ConnectNetwork
from hw.mixins.temperature import TemperatureUnit
from .base import BaseState


class Measurement(BaseState):
    name = "Measurement"

    def exec(self):
        now = RTC().datetime()

        temperature = self.context.temperature_sensor.temperature(unit=TemperatureUnit.METRIC)
        print(f'Current Temperature is {temperature}')

        sleep(1)

        humidity = self.context.humidity_sensor.humidity()
        print(f'Current Humidity is {humidity}')

        with open(METRICS_FILE, "a") as file:
            print(f'{to_iso8601(now)};{temperature};{TemperatureUnit.METRIC};{humidity}', file=file)

        return ConnectNetwork(self.context)
