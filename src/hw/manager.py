__all__ = ['DeviceManager']


class DeviceManager:
    def __init__(self):
        self._devices = []

    def register(self, device):
        self._devices.append(device)

    def get(self, device_type):
        for device in self._devices:
            if isinstance(device, device_type):
                return device
        return None

    def all(self, device_type=None):
        if device_type is None:
            return list(self._devices)
        return [d for d in self._devices if isinstance(d, device_type)]
