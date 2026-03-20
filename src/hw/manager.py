__all__ = ['DeviceManager']


class DeviceManager:
    """Registry for hardware devices.

    Provides a central place to register and retrieve BaseDevice instances.
    Devices can be looked up by type, mixin, or alias. The manager is iterable
    and supports index-based access.

    Example:
        manager = DeviceManager()
        manager.register(WS2812B(18, 1, alias='diag_led'))
        manager.register(DHT11(3))

        manager.get('diag_led')        # by alias
        manager.get(WS2812B)           # first device of given type
        manager.get(TemperatureMixin)  # first device with given capability
        manager[0]                     # by index
    """

    def __init__(self):
        self._devices = []

    def register(self, device):
        """Register a device.

        Args:
            device: A BaseDevice instance to register.

        Raises:
            ValueError: If a device with the same alias is already registered.
        """
        existing_aliases = {a for d in self._devices for a in d.aliases}
        for alias in device.aliases:
            if alias in existing_aliases:
                raise ValueError(f'Device with alias "{alias}" already registered.')
        self._devices.append(device)

    def get(self, device_type_or_alias):
        """Retrieve the first device matching the given type or alias.

        Args:
            device_type_or_alias: A string alias or a class (type or mixin).

        Returns:
            The first matching BaseDevice instance, or None if not found.
        """
        if isinstance(device_type_or_alias, str):
            for device in self._devices:
                if device_type_or_alias in device.aliases:
                    return device
            return None
        for device in self._devices:
            if isinstance(device, device_type_or_alias):
                return device
        return None

    def all(self, device_type=None) -> list:
        """Return all registered devices, optionally filtered by type or mixin.

        Args:
            device_type: Optional class to filter by. If None, all devices
                         are returned.

        Returns:
            List of matching BaseDevice instances.
        """
        if device_type is None:
            return list(self._devices)
        return [d for d in self._devices if isinstance(d, device_type)]

    def __iter__(self):
        return iter(self._devices)

    def __len__(self):
        return len(self._devices)

    def __getitem__(self, index):
        return self._devices[index]
