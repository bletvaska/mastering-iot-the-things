import machine

from constants import SETTINGS_FILE, SALT_FILE
from .base import BaseState


class FactoryReset(BaseState):
    name = "Factory Reset"

    def exec(self):
        # cleanup
        SETTINGS_FILE.unlink(missing_ok=True)
        SALT_FILE.unlink(missing_ok=True)

        # hard reset
        machine.reset()
