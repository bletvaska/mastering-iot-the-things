from states.sleep import Sleep
from helpers import do_connect
from .base import BaseState


class ConnectNetwork(BaseState):
    def exec(self):
        wifi = self.context.settings.wifi

        do_connect(wifi.ssid, wifi.password)

        return Sleep(self.context)
