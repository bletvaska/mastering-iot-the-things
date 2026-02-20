from commands.base import BaseCommand


class Version(BaseCommand):
    name = 'version'
    description = 'Show version'

    def exec(self) -> None:
        self.context.uart.write('Version 2026.1\r\n')
