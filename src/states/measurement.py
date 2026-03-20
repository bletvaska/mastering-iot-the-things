from time import sleep

from helpers import to_iso8601
from machine import RTC

from constants import METRICS_FILE, ALIAS_RTC, ALIAS_TEMP, ALIAS_HUMIDITY
from .connect_network import ConnectNetwork
from hw.mixins.sensors.humidity import HumidityMixin
from hw.mixins.sensors.temperature import TemperatureMixin, TemperatureUnit
from .base import BaseState


class Measurement(BaseState):
    name = "Measurement"

    def exec(self):
        rtc = self.context.devices.get(ALIAS_RTC)
        now = rtc.datetime()

        temperature = self.context.devices.get(ALIAS_TEMP).temperature(unit=TemperatureUnit.METRIC)
        print(f'Current Temperature is {temperature}')

        humidity = self.context.devices.get(ALIAS_HUMIDITY).humidity()
        print(f'Current Humidity is {humidity}')

        with open(METRICS_FILE, "a") as file:
            print(f'{to_iso8601(now)};{temperature};{TemperatureUnit.METRIC};{humidity}', file=file)

        return ConnectNetwork(self.context)
