from machine import Pin

from hw.base import BaseDevice
from hw.mixins.sensors.button import ButtonMixin


class Button(ButtonMixin, BaseDevice):
    name = 'Button'
    description = 'Push button'

    def __init__(self, pin: int, alias=None):
        BaseDevice.__init__(self, alias)
        self.pins = {'data': pin}
        self._pin = Pin(pin, Pin.IN, Pin.PULL_UP)

    def is_pressed(self) -> bool:
        return not self._pin.value()
