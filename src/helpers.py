import json

from constants import SETTINGS_FILE

from models.settings import Settings


def get_settings() -> Settings:
    with open(SETTINGS_FILE, 'r') as file:
        settings = json.load(file)
        return Settings(**settings)


def do_connect(ssid: str, password: str):
    import machine, network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print(f'Connecting to network {ssid}...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            machine.idle()

    print('network config:', wlan.ipconfig('addr4'))

    import ntptime
    ntptime.settime()
    print(machine.RTC().datetime())


def to_yaml(data: dict, indent: int = 0) -> str:
    lines = []
    prefix = '  ' * indent

    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f'{prefix}{key}:')
            lines.append(to_yaml(value, indent + 1))
        elif value is None:
            lines.append(f'{prefix}{key}:')
        elif isinstance(value, bool):
            lines.append(f'{prefix}{key}: {str(value).lower()}')
        elif isinstance(value, str):
            lines.append(f'{prefix}{key}: "{value}"')
        else:
            lines.append(f'{prefix}{key}: {value}')

    return '\n'.join(lines)


def to_iso8601(dt: tuple) -> str:
    return f'{dt[0]}-{dt[1]:02}-{dt[2]:02}T{dt[4]:02}:{dt[5]:02}:{dt[6]:02}Z'
