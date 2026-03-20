import machine

from constants import SETTINGS_FILE
from .base import BaseState


class FactoryReset(BaseState):
    name = "Factory Reset"

    def exec(self):
        SETTINGS_FILE.unlink(missing_ok=True)
        machine.reset()
