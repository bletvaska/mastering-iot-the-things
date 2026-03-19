from os import dupterm
from machine import UART, Pin

from commands.blink import Blink
from commands.power import Power
from commands.rtc import RTC
from commands.commands import Commands
from commands.devices import Devices
from commands.help import Help
from commands.network import Network
from commands.reset import Reset
from commands.settings import Settings
from commands.sysinfo import SysInfo
from commands.uptime import Uptime
from commands.version import Version
from constants import UART_TX_PIN, UART_RX_PIN
from hw.ws2812b import WS2812B
from states.base import BaseState


class ServiceTerminal(BaseState):
    name = 'Service Terminal'

    def enter(self):
        self.context.devices.get(WS2812B).set_color(5, 5, 5)

        self.context.parser.register(Blink(self.context))
        self.context.parser.register(Commands(self.context))
        self.context.parser.register(Devices(self.context))
        self.context.parser.register(Help(self.context))
        self.context.parser.register(Network(self.context))
        self.context.parser.register(Power(self.context))
        self.context.parser.register(Reset(self.context))
        self.context.parser.register(Settings(self.context))
        self.context.parser.register(SysInfo(self.context))
        self.context.parser.register(RTC(self.context))
        self.context.parser.register(Uptime(self.context))
        self.context.parser.register(Version(self.context))

        # initialization of UART0 for serial console
        uart = UART(0, baudrate=115200, tx=Pin(UART_TX_PIN), rx=Pin(UART_RX_PIN), rxbuf=100)
        dupterm(uart)

    def exec(self):
        print('# Welcome to Service Terminal')

        while True:
            # try:
                line = input('> ').strip()

                if line == '':
                    continue

                result = self.context.parser.parse(line)
                if result is None:
                    print('Unknown command')
                else:
                    cmd, params = result
                    cmd(params)
                    print()
            # except KeyboardInterrupt:
            #     pass
