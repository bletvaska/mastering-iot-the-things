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
    0x5F: 'AT24C32 (EEPROM)',
    0x68: 'DS3231 (RTC)',
    0x76: 'BME280 / BMP280',
    0x77: 'BME280 / BMP280',
}


class I2C(BaseCommand):
    name = 'i2c'
    description = 'I2C bus management.'
    usage = (
        ('i2c scan', 'Scan for devices on the I2C bus.'),
        ('i2c read <addr> <reg> <n>', 'Read n bytes from device address at register.'),
        ('i2c write <addr> <reg> <byte...>', 'Write bytes to device address at register.'),
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
            'read': self._read,
            'write': self._write,
        }

        handler = dispatch.get(params[0])
        if handler:
            handler(params[1:])
        else:
            print('Error: Wrong Usage')
            print(self)

    def _write(self, params):
        if len(params) < 3:
            print('Error: Wrong Usage')
            print(self)
            return

        try:
            addr = int(params[0], 0)
            reg  = int(params[1], 0)
            data = bytes(int(b, 0) for b in params[2:])
        except ValueError:
            print('Error: Invalid argument.')
            return

        try:
            self._i2c.writeto_mem(addr, reg, data)
        except OSError as e:
            print(f'Error: {e}')
            return

        hex_bytes = ' '.join(f'{b:02x}' for b in data)
        print(f'[{hex(addr)}] reg {hex(reg)} <- {hex_bytes}')

    def _read(self, params):
        if len(params) != 3:
            print('Error: Wrong Usage')
            print(self)
            return

        try:
            addr = int(params[0], 0)
            reg  = int(params[1], 0)
            n    = int(params[2])
        except ValueError:
            print('Error: Invalid argument.')
            return

        try:
            data = self._i2c.readfrom_mem(addr, reg, n)
        except OSError as e:
            print(f'Error: {e}')
            return

        print(f'[{hex(addr)}] reg {hex(reg)}:')
        chunk_size = 8
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            hex_part = ' '.join(f'{b:02x}' for b in chunk)
            asc_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            print(f'  {hex_part:<23}  |{asc_part}|')

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
