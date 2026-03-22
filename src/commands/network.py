from exceptions import NetworkError
from .base import BaseCommand
from constants import ALIAS_WIFI


class Network(BaseCommand):
    name = 'net'
    description = 'Network interface management.'
    usage = (
        ('net connect <ssid> <password>', 'Connect to network.'),
        ('net disconnect', 'Disconnect from network.'),
        ('net stat', 'Connection status.'),
        ('net ping <host> [count]', 'Ping a host.'),
        ('net scan', 'Scan networks.'),
        ('net deactivate', 'Deinitialize interface.'),
    )

    def __call__(self, params: list) -> None:
        if len(params) == 0:
            print(self)
            return

        self.dispatch = {
            'stat': self._stat,
            'scan': self._scan,
            'connect': self._connect,
            'ping': self._ping,
            'disconnect': self._disconnect,
            'deactivate': self._deactivate,
        }

        handler = self.dispatch.get(params[0])
        if handler:
            handler(self.context.devices.get(ALIAS_WIFI), params[1:])
        else:
            print("Error: Wrong Usage")
            print(self)

    def _deactivate(self, wlan, params):
        if wlan.active():
            print('Deactivating interface.')
            wlan.deinit()

    def _disconnect(self, wlan, params):
        if wlan.isconnected():
            print('Disconnecting from network...')
            wlan.disconnect()

    def _stat(self, wlan, params):
        status_names = {
            0: 'idle',
            1: 'connecting',
            3: 'connected',
            -1: 'connection failed',
            -2: 'no AP found',
            -3: 'wrong password',
        }

        active = wlan.active()
        status = status_names.get(wlan.status(), str(wlan.status()))
        mac = ':'.join('%02x' % b for b in wlan.config('mac'))

        print(f"{'Active':<10}: {'yes' if active else 'no'}")
        print(f"{'Status':<10}: {status}")
        print(f"{'MAC':<10}: {mac}")

        if active and wlan.isconnected():
            import network
            rssi = wlan.status('rssi')
            print(f"{'SSID':<10}: {wlan.config('ssid')}")
            print(f"{'Channel':<10}: {wlan.config('channel')}")
            print(f"{'RSSI':<10}: {rssi} dBm")
            ip, mask = wlan.ipconfig('addr4')
            print(f"{'IP':<10}: {ip}")
            print(f"{'Mask':<10}: {mask}")
            print(f"{'Gateway':<10}: {wlan.ipconfig('gw4')}")
            print(f"{'DNS':<10}: {network.ipconfig('dns')}")

    def _scan(self, wlan, params):
        security_names = {0: 'open', 1: 'WEP', 2: 'WPA-PSK', 3: 'WPA2-PSK', 4: 'WPA/WPA2-PSK'}

        wlan.active(True)
        results = wlan.scan()

        print(f"{'SSID':<32}  {'CH':>3}  {'RSSI':>5}  {'SECURITY':<13}  HIDDEN")
        print(f"{'-' * 32}  {'-' * 3}  {'-' * 5}  {'-' * 13}  {'-' * 6}")
        for result in results:
            ssid = result[0].decode('utf-8')
            channel = result[2]
            rssi = result[3]
            security = security_names.get(result[4], str(result[4]))
            hidden = 'yes' if result[5] else 'no'
            print(f"{ssid:<32}  {channel:>3}  {rssi:>5}  {security:<13}  {hidden}")

    def _connect(self, wlan, params):
        if len(params) != 2:
            print("Error: Wrong Usage")
            print(self)
            return

        ssid, password = params
        print(f'Connecting to {ssid}...')

        try:
            wlan.connect(ssid, password)

            import network
            ip, mask = wlan.ipconfig('addr4')
            print(f"{'SSID':<10}: {wlan.config('ssid')}")
            print(f"{'IP':<10}: {ip}")
            print(f"{'Mask':<10}: {mask}")
            print(f"{'Gateway':<10}: {wlan.ipconfig('gw4')}")
            print(f"{'DNS':<10}: {network.ipconfig('dns')}")
        except NetworkError as ex:
            print(f'Network Error: {ex}')

    def _ping(self, wlan, params):
        if not (1 <= len(params) <= 2):
            print("Error: Wrong Usage")
            print(self)
            return

        if not wlan.isconnected():
            print('Not connected.')
            return

        import lib.uping as uping

        host = params[0]
        count = int(params[1]) if len(params) == 2 else 4
        uping.ping(host, count=count)
