from time import sleep

from .base import BaseState


class Sleep(BaseState):
    name = "Sleep"

    def exec(self):
        self.context.diag_led.off()

        # disconnect from mqtt
        self.context.mqtt_client.publish(
            f'{self.context.settings.base_topic()}/status',
            '{"status": "offline", "owner": "mirek"}',
            retain=True
        )
        self.context.mqtt_client.disconnect()

        self.context.wlan.disconnect()
        self.context.wlan.deinit()

        sleep(1)  # aby vsetci stihli spravit to, co treba
        # deepsleep()
        return None
