__all__ = ['BaseDevice']


class BaseDevice:
    """Base class for all hardware devices.

    Subclasses represent physical peripherals connected to the microcontroller.
    Each device declares its name, description, and optionally an alias for
    identification within the DeviceManager.

    Capabilities are detected automatically from the class hierarchy — any
    base class whose name ends with 'Mixin' is considered a capability.

    Example:
        class DHT11(TemperatureMixin, HumidityMixin, BaseDevice):
            name = 'DHT11'
            description = 'Temperature and humidity sensor'

            def __init__(self, pin):
                BaseDevice.__init__(self, alias='dht11')
                self.pins = {'data': pin}
    """

    name: str
    description: str

    def __init__(self, alias=None):
        """
        Args:
            alias: Optional unique identifier for this device instance.
                   Used to retrieve the device from DeviceManager by name.
        """
        self.pins = {}
        self.alias = alias

    def capabilities(self) -> list:
        """Return a list of capability mixin names this device implements.

        Capabilities are detected from direct base classes whose name ends
        with 'Mixin'.

        Returns:
            List of mixin class name strings.
        """
        return [cls.__name__ for cls in type(self).__bases__
                if cls.__name__.endswith('Mixin')]

    def test(self) -> list:
        """Run a self-test on this device.

        Should verify the device is operational. Interactive tests may prompt
        the technician for visual or physical confirmation.

        Returns:
            List of dicts with keys 'step' (str) and 'passed' (bool).

        Raises:
            NotImplementedError: If the device does not implement a test.
        """
        raise NotImplementedError(f'Test not implemented for {self.__class__.__name__}.')

    def info(self) -> dict:
        """Return a dictionary with device information.

        Returns:
            Dict with keys: name, alias, description, pins, capabilities.
        """
        return {
            'name': self.name,
            'alias': self.alias,
            'description': self.description,
            'pins': self.pins,
            'capabilities': self.capabilities(),
        }
