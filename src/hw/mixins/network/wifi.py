from .network import NetworkMixin


class WiFiMixin(NetworkMixin):
    def connect(self, ssid=None, key=None, *, bssid=None):
        """Connect to a wireless network.

        ssid: network name
        key: password / authentication key
        bssid: optional MAC address of a specific access point to connect to
        """
        raise NotImplementedError

    def disconnect(self):
        """Disconnect from the current wireless network."""
        raise NotImplementedError

    def scan(self) -> list:
        """Scan for available wireless networks.

        Returns a list of tuples:
            (ssid, bssid, channel, rssi, security, hidden)

        Security values:
            0 = open
            1 = WEP
            2 = WPA-PSK
            3 = WPA2-PSK
            4 = WPA/WPA2-PSK
        """
        raise NotImplementedError
