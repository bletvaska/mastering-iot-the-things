import machine

from constants import I2C_SDA_PIN, I2C_SCL_PIN
from .base import BaseCommand

_KNOWN_DEVICES = {
    0x20: 'PCF8574 (I/O expander)',
    0x27: 'PCF8574 (I/O expander)',
    0x3C: 'SSD1306 (OLED display)',
    0x3D: 'SSD1306 (OLED display)',
    0x48: 'ADS1115 / TMP102',
    0x57: 'AT24C32 (EEPROM)',
    0x68: 'DS3231 (RTC)',
    0x76: 'BME280 / BMP280',
    0x77: 'BME280 / BMP280',
}


class I2C(BaseCommand):
    name = 'i2c'
    description = 'I2C bus management.'
    usage = (
        ('i2c scan', 'Scan for devices on the I2C bus.'),
    )

    def __init__(self, context):
        super().__init__(context)
        self._i2c = machine.I2C(sda=I2C_SDA_PIN, scl=I2C_SCL_PIN)

    def __call__(self, params: list) -> None:
        if len(params) == 0:
            print(self)
            return

        dispatch = {
            'scan': self._scan,
        }

        handler = dispatch.get(params[0])
        if handler:
            handler(params[1:])
        else:
            print('Error: Wrong Usage')
            print(self)

    def _scan(self, params):
        addresses = self._i2c.scan()

        if not addresses:
            print('No devices found.')
            return

        print(f'Found {len(addresses)} device(s):\n')
        print(f'  {"ADDRESS":<10}  DEVICE')
        print(f'  {"-" * 10}  {"-" * 24}')
        for addr in addresses:
            known = _KNOWN_DEVICES.get(addr, '')
            print(f'  {hex(addr):<10}  {known}')
