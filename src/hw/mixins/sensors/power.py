class BatteryVoltageMixin:
    def battery_voltage(self) -> float:
        """Return the current battery voltage in volts (V).

        :return: Battery voltage as a floating-point value.
        :raises NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError


class BatteryMixin:
    def battery_percent(self) -> float:
        """Return the estimated battery charge level (0.0–100.0 %).

        The calculation depends on the battery type and discharge curve.

        :return: Battery level as a floating-point percentage.
        :raises NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError


class ChargingMixin:
    """
    Mixin for devices capable of reporting charging state.
    """
    def is_charging(self) -> bool:
        """Return True if the battery is currently charging."""
        raise NotImplementedError


class PowerSource:
    BATTERY  = 'battery'
    USB      = 'usb'
    EXTERNAL = 'external'
    UNKNOWN  = 'unknown'


class PowerSourceMixin:
    def power_source(self) -> PowerSource:
        """Return the current power source.

        :return: One of the PowerSource constants.
        :raises NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError
