from .base import BaseCommand
from constants import ALIAS_WIFI


class Network(BaseCommand):
    name = 'net'
    description = 'Network interface management.'
    usage = (
        ('net connect <ssid> <password>', 'Connect to network.'),
        ('net disconnect', 'Disconnect from  network.'),
        ('net stat', 'Connection status.'),
        ('net deactivate', 'Deinitialize interface.'),
        ('net scan', 'Scan networks.'),
    )

    def __call__(self, params: list) -> None:
        if len(params) == 0:
            print('Error: Wrong Usage')
            print(self)
            return

        wlan = self.context.devices.get(ALIAS_WIFI)

        if params[0] == 'stat':
            if wlan.active() is False:
                print('WLAN not activated.')
            else:
                print('WLAN is active.')
                print('Connected:', wlan.isconnected())
                if wlan.isconnected():
                    print('network config:', wlan.ipconfig('addr4'))
                    print('ssid:', wlan.config('ssid'))

        elif params[0] == 'scan':
            wlan.active(True)
            for result in wlan.scan():
                print(result[0].decode('utf-8'), result[2], result[4], result[5])

        elif params[0] == 'connect':
            if len(params) != 3:
                print("Error: Wrong Usage")
                print(self)
                return

            ssid, password = params[1:3]
            wlan.connect(ssid, password)

        elif params[0] == 'disconnect':
            if wlan.isconnected():
                print('Disconnecting from network...')
                wlan.disconnect()

        elif params[0] == 'deactivate':
            if wlan.active():
                print('Deactivating interface.')
                wlan.deinit()
