from pathlib import Path

# pins configuration
DHT_PIN = 3
BTN_PIN = 20
DIAG_LED_PIN = 18
SVC_PIN = 16

UART_TX_PIN = 16
UART_RX_PIN = 17

I2C_SDA_PIN = 4  # I2C data line (SDA)
I2C_SCL_PIN = 5  # I2C clock line (SCL)
RTC_ALARM_PIN = 2  # GPIO pin for RTC alarm signal

# paths
DATA_FOLDER = Path('/data')
SETTINGS_FILE = DATA_FOLDER / 'settings.json'
METRICS_FILE = DATA_FOLDER / 'metrics.csv'
SALT_FILE = DATA_FOLDER / '.salt'

# device aliases
ALIAS_WIFI        = 'wifi'
ALIAS_DIAG_LED    = 'diag_led'
ALIAS_CONTROL_BTN = 'control_btn'
ALIAS_SERVICE_BTN = 'service_btn'
ALIAS_POWER       = 'power'
ALIAS_RTC         = 'rtc'
ALIAS_TEMP        = 'temp'
ALIAS_HUMIDITY    = 'humidity'

# durations
SHORT_PRESS_DURATION = 2 * 1000
LONG_PRESS_DURATION = 6 * 1000
