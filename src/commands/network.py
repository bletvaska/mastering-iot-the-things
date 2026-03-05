from commands.base import BaseCommand
import machine


class Network(BaseCommand):
    name = 'net'
    description = 'Network interface management.'
    usage = (
        ('net connect', 'Connect to network.'),
        ('net disconnect', 'Disconnect from  network.'),
        ('net stat', 'Connection status.'),
        ('net deactivate', 'Deinitialize interface.'),
        ('net scan', 'Scan networks.'),
    )

    def exec(self) -> None:
        if len(self.params) == 0:
            print('Error: Wrong Usage')
            print(self.usage)
            return

        wlan = self.context.wlan

        if self.params[0] == 'stat':
            if wlan.active() is False:
                print('WLAN not activated.')
            else:
                print('WLAN is active.')
                print('Connected:', wlan.isconnected())
                if wlan.isconnected():
                    print('network config:', wlan.ipconfig('addr4'))
                    print('ssid:', wlan.config('ssid'))
                # print('password:', wlan.config('key'))
                # print('hidden:', wlan.config('hidden'))

        elif self.params[0] == 'scan':
            wlan.active(True)
            for network in wlan.scan():
                print(network[0].decode('utf-8'), network[2], network[4], network[5])

        elif self.params[0] == 'connect':
            if len(self.params) != 3:
                print("Error: Wrong Usage")
                print(self.usage)
                return

            if not wlan.isconnected():
                ssid, password = self.params[1:3]
                print(f'Connecting to {ssid}...')

                wlan.active(True)
                wlan.connect(ssid, password)
                while not wlan.isconnected():
                    machine.idle()

            print('network config:', wlan.ipconfig('addr4'))

        elif self.params[0] == 'disconnect':
            if wlan.isconnected():
                print('Disconnecting from network...')
                wlan.disconnect()

        elif self.params[0] == 'deactivate':
            if wlan.active():
                print('Deactivating interface.')
                wlan.active(False)
                wlan.deinit()
