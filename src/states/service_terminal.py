from os import dupterm

from commands.devices import Devices
from commands.help import Help
from commands.commands import Commands
from commands.network import Network
from commands.reset import Reset
from commands.blink import Blink
from commands.settings import Settings
from commands.version import Version
from commands.uptime import Uptime
from machine import UART, Pin
from parser import Parser
from constants import UART_TX_PIN, UART_RX_PIN
from hw.ws2812b import WS2812B
from states.base import BaseState


class ServiceTerminal(BaseState):
    name = 'Service Terminal'

    def enter(self):
        self.context.devices.get(WS2812B).set_color(5, 5, 5)

        self.parser = Parser()
        self.parser.register(Version(self.context))
        self.parser.register(Uptime(self.context))
        self.parser.register(Devices(self.context))
        self.parser.register(Blink(self.context))
        self.parser.register(Settings(self.context))
        self.parser.register(Reset(self.context))
        self.parser.register(Network(self.context))
        self.parser.register(Commands(self.context, self.parser))
        self.parser.register(Help(self.context, self.parser))

        # initialization of UART0 for serial console
        uart = UART(0, baudrate=115200, tx=Pin(UART_TX_PIN), rx=Pin(UART_RX_PIN), rxbuf=100)
        dupterm(uart)

    def exec(self):
        print('# Welcome to Service Terminal')

        while True:
            try:
                line = input('> ').strip()

                # empty line?
                if line == '':
                    continue

                result = self.parser.parse(line)
                if result is None:
                    print('Unknown command')
                else:
                    cmd, params = result
                    cmd(params)
            except KeyboardInterrupt:
                pass
