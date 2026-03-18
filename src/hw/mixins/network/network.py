class NetworkMixin:
    def active(self, is_active=None):
        """Activate or deactivate the network interface.

        Without argument returns current state (bool).
        """
        raise NotImplementedError

    def isconnected(self) -> bool:
        """Return True if the interface has an active network connection."""
        raise NotImplementedError

    def status(self, param=None):
        """Return dynamic status of the network interface.

        Without argument returns the link status. With a string param returns
        the value of that specific status parameter.
        """
        raise NotImplementedError

    def ipconfig(self, param=None, **kwargs):
        """Get or set IP configuration parameters.

        Called with a string param returns that parameter's value.
        Called with keyword arguments sets those parameters.
        Common params: dhcp4, addr4, gw4, dns.
        """
        raise NotImplementedError

    def config(self, param=None, **kwargs):
        """Get or set general network interface parameters.

        Called with a string param returns that parameter's value.
        Called with keyword arguments sets those parameters.
        """
        raise NotImplementedError

    def deinit(self):
        """Shut down and release the network hardware module."""
        raise NotImplementedError
