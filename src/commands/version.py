from .base import BaseCommand
from version import VERSION, BUILD_DATE, BOARD


class Version(BaseCommand):
    name = 'version'
    description = 'Show version'

    def __call__(self, params: list) -> None:
        print(f'Version   : {VERSION}')
        print(f'Build date: {BUILD_DATE}')
        print(f'Board     : {BOARD}')
