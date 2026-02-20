from constants import DIAG_LED_PIN
from machine import Pin
from neopixel import NeoPixel

from states.init import Init


class Context:
    def __init__(self):
        self.state = Init(self)

        pin = Pin(DIAG_LED_PIN, Pin.OUT)
        self.diag_led = NeoPixel(pin, 1)

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
