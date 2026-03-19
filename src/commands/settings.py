from models.settings import Settings
from .base import BaseCommand
from constants import SETTINGS_FILE
from helpers import to_yaml, get_settings


class Settings(BaseCommand):
    name = 'settings'
    description = 'User settings management.'
    usage = (
        ('settings show', 'shows user settings'),
        ('settings set <key> <value>', 'sets settings key'),
        ('settings get <key>', 'gets settings value'),
        ('settings save', 'save settings'),
        ('settings load', 'load settings'),
    )

    def __init__(self, context):
        super().__init__(context)

        self.dispatch = {
            'show': self._show,
            'get': self._get,
            'set': self._set,
            'load': self._load,
            'save': self._save,
        }

    def __call__(self, params: list) -> None:
        if self.context.settings is None:
            print('No settings loaded.')
            return

        if len(params) == 0:
            print(self)
            return

        handler = self.dispatch.get(params[0])
        if handler:
            handler(params[1:])
        else:
            print("Error: Wrong Usage")
            print(self)

    def _get(self, params: list):
        pass

    def _set(self, params: list):
        pass

    def _show(self, params: list):
        print(to_yaml(self.context.settings.model_dump()))

    def _load(self, params: list):
        try:
            self.context.settings = get_settings()
            print('Settings loaded.')
        except OSError:
            print('Error: Settings file not found.')

    def _save(self, params: list):
        self.context.settings.save(SETTINGS_FILE)
        print('Settings saved.')
