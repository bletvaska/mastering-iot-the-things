from machine import Pin
from neopixel import NeoPixel

from hw.base import BaseDevice
from hw.mixins.actuators.colorlight import ColorlightMixin
from hw.mixins.actuators.onoff import OnOffMixin


class WS2812B(OnOffMixin, ColorlightMixin, BaseDevice):
    name = 'WS2812B'
    description = 'RGB LED controller'

    def __init__(self, pin: int, number: int):
        BaseDevice.__init__(self)
        self.pins = {'data': pin}
        self.np = NeoPixel(Pin(pin, Pin.OUT), number)
        self.color = (255, 255, 255)

    def on(self):
        self.np.fill(self.color)
        self.np.write()

    def off(self):
        self.np.fill((0, 0, 0))
        self.np.write()

    def toggle(self):
        if self.np[0] == (0, 0, 0):
            self.on()
        else:
            self.off()

    def set_color(self, r, g, b):
        self.color = (r, g, b)
        self.np.fill(self.color)
        self.np.write()

    def color(self):
        return self.color
