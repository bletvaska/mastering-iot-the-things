from states.init import Init
from context import Context
from hw.button import Button
from hw.cyw43439 import CYW43439
from hw.power_monitor import PowerMonitor
from hw.dht11 import DHT11
# from hw.dht22 import DHT22
from hw.ds3231 import DS3231
from hw.manager import DeviceManager
from hw.ws2812b import WS2812B
from constants import DIAG_LED_PIN, BTN_PIN, DHT_PIN, SVC_PIN, I2C_SDA_PIN, I2C_SCL_PIN, RTC_ALARM_PIN, ALIAS_WIFI, ALIAS_DIAG_LED, ALIAS_CONTROL_BTN, ALIAS_SERVICE_BTN, ALIAS_POWER, ALIAS_RTC, ALIAS_TEMP, ALIAS_HUMIDITY


def register_devices() -> DeviceManager:
    """Create a device manager with all devices this smart device is built from."""
    devices = DeviceManager()
    devices.register(WS2812B(DIAG_LED_PIN, 1, alias=ALIAS_DIAG_LED))
    devices.register(DHT11(DHT_PIN, alias=[ALIAS_TEMP, ALIAS_HUMIDITY]))
    devices.register(DS3231(I2C_SDA_PIN, I2C_SCL_PIN, RTC_ALARM_PIN, alias=ALIAS_RTC))
    devices.register(CYW43439(alias=ALIAS_WIFI))
    devices.register(Button(BTN_PIN, alias=ALIAS_CONTROL_BTN))
    devices.register(Button(SVC_PIN, alias=ALIAS_SERVICE_BTN))
    devices.register(PowerMonitor(alias=ALIAS_POWER))
    return devices


if __name__ == "__main__":
    # monkey-patching of builtin open() for reading the Path objects
    import builtins

    _original_open = builtins.open

    def _patched_open(file, *args, **kwargs):
        if not isinstance(file, (str, bytes)):
            file = str(file)
        return _original_open(file, *args, **kwargs)

    builtins.open = _patched_open

    # run
    thsensor = Context(register_devices(), Init)
    thsensor.run()
