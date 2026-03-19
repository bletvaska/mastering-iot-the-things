import network
from machine import idle

from hw.base import BaseDevice
from hw.mixins.network.network import NetworkMixin
from hw.mixins.network.wifi import WiFiMixin


class CYW43439(BaseDevice, NetworkMixin, WiFiMixin):
    name = 'CYW43439'
    description = 'Built-in WiFi module (Raspberry Pi Pico 2 W)'

    def __init__(self, alias=None):
        BaseDevice.__init__(self, alias)
        self.pins = {
            'clk': 29,
            'data': 24,  # shared MOSI / MISO / IRQ (half-duplex)
            'cs': 25,
            'power_enable': 23,
            'led': 'WL_GPIO0',
            'smps_pwm': 'WL_GPIO1',
            'vbus': 'WL_GPIO2',
        }
        self._wlan = network.WLAN(network.STA_IF)

    def active(self, is_active=None) -> bool | None:
        if is_active is None:
            return self._wlan.active()
        self._wlan.active(is_active)

    def connect(self, ssid=None, key=None, *, bssid=None):
        self._wlan.active(True)

        if not self._wlan.isconnected():
            self._wlan.connect(ssid, key, bssid=bssid)
            while not self._wlan.isconnected():
                idle()

    def disconnect(self):
        self._wlan.disconnect()

    def isconnected(self) -> bool:
        return self._wlan.isconnected()

    def scan(self) -> list:
        return self._wlan.scan()

    def status(self, param=None):
        if param is None:
            return self._wlan.status()
        return self._wlan.status(param)

    def ipconfig(self, param=None, **kwargs):
        if param is not None:
            return self._wlan.ipconfig(param)
        if kwargs:
            self._wlan.ipconfig(**kwargs)

    def config(self, param=None, **kwargs):
        if param is not None:
            return self._wlan.config(param)
        if kwargs:
            self._wlan.config(**kwargs)

    def deinit(self):
        self._wlan.active(False)
        self._wlan.deinit()
