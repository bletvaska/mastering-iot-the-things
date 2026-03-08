import os
import machine

from constants import SETTINGS_FILE
from .base import BaseState


class FactoryReset(BaseState):
    name = "Factory Reset"

    def exec(self):
        try:
            os.remove(SETTINGS_FILE)
        except OSError as e:
            print(f'>> Could not remove settings file: {e}')
        machine.reset()
