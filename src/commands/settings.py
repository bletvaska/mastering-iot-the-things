from .base import BaseCommand
from constants import SETTINGS_FILE, SALT_FILE
from crypto import encrypt
from helpers import to_yaml, get_settings


class Settings(BaseCommand):
    name = 'settings'
    description = 'User settings management.'
    usage = (
        ('settings show', 'shows user settings'),
        ('settings set <key> <value>', 'sets settings key'),
        ('settings get <key>', 'gets settings value'),
        ('settings passwd <key> <value>', 'sets and encrypts a password field'),
        ('settings save', 'save settings'),
        ('settings load', 'load settings'),
    )

    def __init__(self, context):
        super().__init__(context)

        self.dispatch = {
            'show': self._show,
            'get': self._get,
            'set': self._set,
            'passwd': self._passwd,
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
        if len(params) != 1:
            print('Error: Wrong Usage')
            print(self)
            return

        data = self.context.settings.model_dump()
        for key in params[0].split('.'):
            if not isinstance(data, dict) or key not in data:
                print(f'Error: Key "{params[0]}" not found.')
                return
            data = data[key]

        print(to_yaml(data) if isinstance(data, dict) else data)

    def _set(self, params: list):
        if len(params) != 2:
            print('Error: Wrong Usage')
            print(self)
            return

        path, value = params
        keys = path.split('.')

        obj = self.context.settings
        for key in keys[:-1]:
            if not hasattr(obj, key):
                print(f'Error: Key "{path}" not found.')
                return
            obj = getattr(obj, key)

        last_key = keys[-1]
        if not hasattr(obj, last_key):
            print(f'Error: Key "{path}" not found.')
            return

        current = getattr(obj, last_key)

        if not isinstance(current, (str, int, float, bool, type(None))):
            print(f'Error: "{path}" is a section, not a value.')
            return

        if isinstance(current, bool):
            value = value.lower() in ('true', '1', 'yes')
        elif isinstance(current, int):
            value = int(value)
        elif isinstance(current, float):
            value = float(value)

        setattr(obj, last_key, value)
        print(f'{path} = {getattr(obj, last_key)}')

    # FIXME
    def _passwd(self, params: list):
        if len(params) != 2:
            print('Error: Wrong Usage')
            print(self)
            return

        path, plaintext = params
        keys = path.split('.')

        if keys[-1] != 'password':
            print(f'Error: "{path}" is not a password field.')
            return

        obj = self.context.settings
        for key in keys[:-1]:
            if not hasattr(obj, key):
                print(f'Error: Key "{path}" not found.')
                return
            obj = getattr(obj, key)

        if not hasattr(obj, 'password'):
            print(f'Error: Key "{path}" not found.')
            return

        print(f'>{plaintext}<')
        setattr(obj, 'password', encrypt(plaintext, SALT_FILE))
        print(f'Password in {path} has been updated.')

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
