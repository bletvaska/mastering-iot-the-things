from machine import Pin
from network import WLAN

from hw.dht11 import DHT11
from hw.mixins.sensors.humidity import HumidityMixin
from hw.mixins.sensors.temperature import TemperatureMixin
from hw.ws2812b import WS2812B
from constants import DIAG_LED_PIN, BTN_PIN, DHT_PIN, SVC_PIN
from models.settings import Settings
from states.init import Init


class Context:
    def __init__(self, initial_state=Init):
        self.state = initial_state(self)

        self.diag_led = WS2812B(DIAG_LED_PIN, 1)

        self.btn = Pin(BTN_PIN, Pin.IN)

        sensor = DHT11(DHT_PIN)
        self.humidity_sensor: HumidityMixin = sensor
        self.temperature_sensor: TemperatureMixin = sensor

        self.terminal = Pin(SVC_PIN, Pin.IN, Pin.PULL_UP)

        self.wlan = WLAN()
        self.settings: Settings = None
        self.mqtt_client = None

    def run(self):
        print(f">> Entering {self.state.name}")
        self.state.enter()
        while True:
            next_state = self.state.exec()

            if next_state is None:
                return

            if next_state is not self.state:
                print(f">> Leaving {self.state.name}")
                self.state.exit()
                self.state = next_state
                print(f">> Entering {self.state.name}")
                self.state.enter()
