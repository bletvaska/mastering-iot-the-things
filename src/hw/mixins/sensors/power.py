class BatteryMixin:
    def battery_voltage(self) -> float:
        raise NotImplementedError


class PowerSourceMixin:
    def is_usb_powered(self) -> bool:
        raise NotImplementedError
