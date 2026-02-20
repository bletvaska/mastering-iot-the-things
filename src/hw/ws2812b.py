from machine import Pin
from neopixel import NeoPixel

from hw.mixins.colorlight import ColorlightMixin
from hw.mixins.onoff import OnOffMixin


class WS2812B(OnOffMixin, ColorlightMixin):
    def __init__(self, pin, number):
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
