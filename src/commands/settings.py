import json

from .base import BaseCommand
from constants import SETTINGS_FILE


class Settings(BaseCommand):
    name = 'settings'
    description = 'User settings management.'
    usage = (
        ('settings show', 'shows user settings'),
        ('settings set <key> <value>', 'sets settings key'),
        ('settings get <key>', 'gets settings value'),
    )

    def exec(self, params: list) -> None:
        if self.context.settings is None:
            print('No settings loaded.')
            return

        if len(params) == 0:
            print(self)
            return

        subcmd = params[0]

        if subcmd == 'show':
            settings = self.context.settings.model_dump()
            print(json.dumps(settings))
        else:
            print('Wrong usage.')
            print(self)
