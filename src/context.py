from time import ticks_ms

from exceptions import THSensorException
from hw.manager import DeviceManager
from models.settings import Settings
from parser import Parser
from states.error import Error
from states.init import Init


class Context:
    def __init__(self, devices: DeviceManager, initial_state=Init):
        """
        Args:
            devices: Device manager with all devices already registered.
            initial_state: State class the state machine starts in.
        """
        self.state = initial_state(self)
        self.devices = devices

        self.started_at = ticks_ms()
        self.parser = Parser()
        self.settings: Settings | None = None
        self.mqtt_client = None

    def run(self):
        print(f">> Entering {self.state.name}")
        self.state.enter()
        while True:
            try:
                next_state = self.state.exec()
            except THSensorException as ex:
                if isinstance(self.state, Error):
                    return  # no handling on error, just quit
                next_state = Error(self, ex)

            if next_state is None:
                return

            if next_state is not self.state:
                print(f">> Leaving {self.state.name}")
                self.state.exit()
                self.state = next_state
                print(f">> Entering {self.state.name}")
                self.state.enter()
