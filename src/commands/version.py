from .base import BaseCommand
from version import VERSION


class Version(BaseCommand):
    name = 'version'
    description = 'Show version'

    def exec(self) -> None:
        print(f'Version: {VERSION}')
