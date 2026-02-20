from hw.mixins.onoff import OnOffMixin
from hw.ws2812b import WS2812B

from constants import DIAG_LED_PIN, BTN_PIN
from machine import Pin

from states.init import Init


class Context:
    def __init__(self):
        self.state = Init(self)

        self.diag_led = WS2812B(DIAG_LED_PIN, 1)

        self.btn = Pin(BTN_PIN, Pin.IN)

    def change_state(self, state):
        self.state = state

    def run(self):
        self.state.enter()
        while True:
            next_state = self.state.exec()

            if next_state is None:
                return

            if next_state is not self.state:
                self.state.exit()
                self.state = next_state
                self.state.enter()
