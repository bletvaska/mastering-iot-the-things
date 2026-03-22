import time

import network
from machine import idle

from exceptions import NetworkError
from hw.base import BaseDevice
from hw.mixins.network.network import NetworkMixin
from hw.mixins.network.wifi import WiFiMixin

MAX_ATTEMPTS = 3
TIMEOUT = 10


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
        attempt = 0

        while attempt < MAX_ATTEMPTS:
            self._wlan.disconnect()
            self._wlan.connect(ssid, key, bssid=bssid)

            attempt += 1
            start = time.ticks_ms()

            while not self._wlan.isconnected():
                status = self._wlan.status()

                # immediate checks
                if status == network.STAT_WRONG_PASSWORD:
                    raise NetworkError("Wrong password")

                if status == network.STAT_NO_AP_FOUND:
                    raise NetworkError("AP not found")

                if status == network.STAT_CONNECT_FAIL:
                    break  # retry

                # timeout of single attempt
                if time.ticks_diff(time.ticks_ms(), start) > TIMEOUT * 1000:
                    break

                # time.sleep(0.2)
                idle()
            else:
                return

            # backoff
            time.sleep(min(2 ** attempt, 10))

        raise NetworkError("Failed to connect")

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
