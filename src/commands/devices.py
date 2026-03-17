from .base import BaseCommand


class Devices(BaseCommand):
    name = 'devices'
    description = 'List all registered hardware devices'

    def __call__(self, params: list) -> None:
        for device in self.context.devices.all():
            info = device.info()
            pins = ', '.join(f'{k}={v}' for k, v in info['pins'].items())
            capabilities = ', '.join(info['capabilities'])
            title = f"{info['name']}"
            if info['alias']:
                title += f" ({info['alias']})"
            print(title)
            print(f"  description : {info['description']}")
            print(f"  pins        : {pins}")
            print(f"  capabilities: {capabilities}")
