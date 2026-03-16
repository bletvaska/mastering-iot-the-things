from .base import BaseCommand
from version import VERSION


class Version(BaseCommand):
    name = 'version'
    description = 'Show version'

    def __call__(self, params: list) -> None:
        print(f'Version: {VERSION}')
