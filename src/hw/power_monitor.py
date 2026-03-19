from machine import ADC, Pin

from hw.base import BaseDevice
from hw.mixins.sensors.power import BatteryMixin, BatteryVoltageMixin, PowerSource, PowerSourceMixin

_LIPO_MIN_V = 3.0
_LIPO_MAX_V = 4.2


class PowerMonitor(PowerSourceMixin, BatteryMixin, BatteryVoltageMixin, BaseDevice):
    name = 'PowerMonitor'
    description = 'Battery and power source monitor'

    def __init__(self, alias=None):
        BaseDevice.__init__(self, alias)
        self.pins = {
            'vbus':    'WL_GPIO2',
            'vsys':    29,        # ADC3, shared with WiFi (requires workaround)
            'vsys_en': 25,        # must be driven high during VSYS measurement
        }
        self._vbus = Pin('WL_GPIO2', Pin.IN) #, Pin.PULL_DOWN)

    def battery_voltage(self) -> float:
        Pin(25, Pin.OUT, value=1)
        Pin(29, Pin.IN, pull=None) # pull=None

        value = ADC(3).read_u16()
        voltage = value * 3 * 3.3 / 65535

        Pin(29, Pin.ALT, pull=Pin.PULL_DOWN, alt=7)
        Pin(25, Pin.OUT, value=0, pull=Pin.PULL_DOWN)

        return voltage

    def battery_percent(self) -> float:
        voltage = self.battery_voltage()
        print(voltage)
        percent = (voltage - _LIPO_MIN_V) / (_LIPO_MAX_V - _LIPO_MIN_V) * 100
        return max(0.0, min(100.0, percent))

    def power_source(self) -> str:
        return PowerSource.USB if self._vbus.value() else PowerSource.BATTERY
