from time import ticks_ms

from hw.button import Button
from hw.cyw43439 import CYW43439
from hw.power_monitor import PowerMonitor
from hw.dht11 import DHT11
from hw.ds3231 import DS3231
from hw.manager import DeviceManager
from hw.ws2812b import WS2812B
from constants import DIAG_LED_PIN, BTN_PIN, DHT_PIN, SVC_PIN, I2C_SDA_PIN, I2C_SCL_PIN, RTC_ALARM_PIN, ALIAS_WIFI, ALIAS_DIAG_LED, ALIAS_CONTROL_BTN, ALIAS_SERVICE_BTN, ALIAS_POWER
from models.settings import Settings
from parser import Parser
from states.init import Init


class Context:
    def __init__(self, initial_state=Init):
        self.state = initial_state(self)

        # initialize device manager and register all available devices
        self.devices = DeviceManager()
        self.devices.register(WS2812B(DIAG_LED_PIN, 1, alias=ALIAS_DIAG_LED))
        self.devices.register(DHT11(DHT_PIN))
        self.devices.register(DS3231(I2C_SDA_PIN, I2C_SCL_PIN, RTC_ALARM_PIN))
        self.devices.register(CYW43439(alias=ALIAS_WIFI))
        self.devices.register(Button(BTN_PIN, alias=ALIAS_CONTROL_BTN))
        self.devices.register(Button(SVC_PIN, alias=ALIAS_SERVICE_BTN))
        self.devices.register(PowerMonitor(alias=ALIAS_POWER))

        self.started_at = ticks_ms()
        self.parser = Parser()
        self.settings: Settings | None = None
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
