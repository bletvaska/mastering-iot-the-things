__all__ = ['DeviceManager']


class DeviceManager:
    def __init__(self):
        self._devices = []

    def register(self, device):
        if device.alias:
            for d in self._devices:
                if d.alias == device.alias:
                    raise ValueError(f'Device with alias "{device.alias}" already registered.')
        self._devices.append(device)

    def get(self, device_type_or_alias):
        if isinstance(device_type_or_alias, str):
            for device in self._devices:
                if device.alias == device_type_or_alias:
                    return device
            return None
        for device in self._devices:
            if isinstance(device, device_type_or_alias):
                return device
        return None

    def all(self, device_type=None):
        if device_type is None:
            return list(self._devices)
        return [d for d in self._devices if isinstance(d, device_type)]
