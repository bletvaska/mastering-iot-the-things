import os
import machine

from constants import SETTINGS_FILE
from .base import BaseState


class FactoryReset(BaseState):
    name = "Factory Reset"

    def exec(self):
        os.remove(SETTINGS_FILE)
        machine.reset()
