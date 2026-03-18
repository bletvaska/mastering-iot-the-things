from machine import Pin
from network import WLAN

from hw.cyw43439 import CYW43439
from hw.dht11 import DHT11
from hw.ds3231 import DS3231
from hw.manager import DeviceManager
from hw.ws2812b import WS2812B
from constants import DIAG_LED_PIN, BTN_PIN, DHT_PIN, SVC_PIN, I2C_SDA_PIN, I2C_SCL_PIN, RTC_ALARM_PIN
from models.settings import Settings
from states.init import Init


class Context:
    def __init__(self, initial_state=Init):
        self.state = initial_state(self)

        self.devices = DeviceManager()
        self.devices.register(WS2812B(DIAG_LED_PIN, 1, alias='diag_led'))
        self.devices.register(DHT11(DHT_PIN))
        self.devices.register(DS3231(I2C_SDA_PIN, I2C_SCL_PIN, RTC_ALARM_PIN))
        self.devices.register(CYW43439(alias='wifi'))

        self.btn = Pin(BTN_PIN, Pin.IN)
        self.wlan = WLAN()
        self.terminal = Pin(SVC_PIN, Pin.IN, Pin.PULL_UP)

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
