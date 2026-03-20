from time import sleep
from machine import lightsleep

from constants import ALIAS_WIFI
from hw.cyw43439 import CYW43439
from .base import BaseState


class Sleep(BaseState):
    name = "Sleep"

    def exec(self):
        from hw.ws2812b import WS2812B
        self.context.devices.get(WS2812B).off()

        # disconnect from mqtt
        self.context.mqtt_client.publish(
            f'{self.context.settings.base_topic()}/status',
            '{"status": "offline", "owner": "mirek"}',
            retain=True
        )
        self.context.mqtt_client.disconnect()

        # shut down wifi
        wlan = self.context.devices.get(ALIAS_WIFI)
        wlan.disconnect()
        wlan.deinit()

        sleep(1)  # aby vsetci stihli spravit to, co treba

        # deepsleep()
        lightsleep(10 * 1000)
        from states.init import Measurement
        return Measurement(self.context)
        # return None
