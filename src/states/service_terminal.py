from machine import UART, Pin
# from commands.bootloader import Bootloader
# from commands.identify import Identify
# from commands.reset import Reset
# from commands.time import Time
# from commands.version import Version
# from parser import Parser
from constants import UART_TX_PIN, UART_RX_PIN
from states.base import BaseState


class ServiceTerminal(BaseState):
    name = 'Service Terminal'

    def enter(self):
        super().enter()
        self.context.diag_led.set_color(5, 5, 5)
    #     self.parser = Parser(self.device)
    #
    #     self.parser.register(Reset(self.device))
    #     self.parser.register(Version(self.device))
    #     self.parser.register(Bootloader(self.device))
    #     self.parser.register(Reset(self.device))
    #     self.parser.register(Time(self.device))
    #     self.parser.register(Version(self.device))
    #     self.parser.register(Identify(self.device))

        # inicializacia UART0 pre seriovú konzolu
        self.uart = UART(0, baudrate=115200, tx=Pin(UART_TX_PIN), rx=Pin(UART_RX_PIN), rxbuf=100)
        self.buffer = ""

    def _read_line(self):
        """Reads one line from UART (terminated by \n or \r\n)"""
        while True:
            if self.uart.any():
                char = self.uart.read(1).decode('utf-8', 'ignore')

                # echo character on UART
                self.uart.write(char)

                if char == '\r' or char == '\n':
                    if self.buffer:
                        line = self.buffer
                        self.buffer = ""
                        self.uart.write('\n')  # new line
                        return line
                    else:
                        self.uart.write('\n')  # on empty enter
                        self.uart.write('> ')  #

                elif char == '\x7f' or char == '\x08':  # backspace or delete
                    if self.buffer:
                        self.buffer = self.buffer[:-1]
                        # remove character on terminal
                        self.uart.write('\b \b')

                else:
                    self.buffer += char

    def exec(self):
        self.uart.write('>> Service Terminal\r\n')

        while True:
            self.uart.write('> ')
            line = self._read_line()
            # output = self.parser.parse(line)
            # if output is not None:
            #     self.uart.write(f'{output}\r\n')
