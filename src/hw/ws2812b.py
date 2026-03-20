from machine import Pin
from neopixel import NeoPixel

from hw.base import BaseDevice
from hw.mixins.actuators.colorlight import ColorlightMixin
from hw.mixins.actuators.onoff import OnOffMixin


class WS2812B(OnOffMixin, ColorlightMixin, BaseDevice):
    name = 'WS2812B'
    description = 'RGB LED controller'

    def __init__(self, pin: int, number: int, alias=None):
        BaseDevice.__init__(self, alias)
        self.pins = {'data': pin}
        self._np = NeoPixel(Pin(pin, Pin.OUT), number)
        self._color = (255, 255, 255)

    def on(self):
        self._np.fill(self._color)
        self._np.write()

    def off(self):
        self._np.fill((0, 0, 0))
        self._np.write()

    def toggle(self):
        if self._np[0] == (0, 0, 0):
            self.on()
        else:
            self.off()

    def color(self, value=None) -> tuple | None:
        if value is None:
            return self._color

        # control content
        if len(value) != 3:
            raise ValueError("r, g, b must be all specified.")

        self._color = value
        self._np.fill(self._color)
        self._np.write()
