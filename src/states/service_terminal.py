from commands.blink import Blink
from commands.config import Config
from commands.version import Version
from machine import UART, Pin
from parser import Parser
from constants import UART_TX_PIN, UART_RX_PIN
from states.base import BaseState


class ServiceTerminal(BaseState):
    name = 'Service Terminal'

    def enter(self):
        super().enter()
        self.context.diag_led.set_color(5, 5, 5)

        self.parser = Parser()
        self.parser.register(Version(self.context))
        self.parser.register(Blink(self.context))
        self.parser.register(Config(self.context))

        # inicializacia UART0 pre seriovú konzolu
        self.context.uart = UART(0, baudrate=115200, tx=Pin(UART_TX_PIN), rx=Pin(UART_RX_PIN), rxbuf=100)
        self.uart = self.context.uart
        # self.buffer = ""

        # redirect REPL to UART
        import os
        os.dupterm(self.uart)

    #
    # def _read_line(self):
    #     """Reads one line from UART (terminated by \n or \r\n)"""
    #     while True:
    #         if self.uart.any():
    #             char = self.uart.read(1).decode('utf-8', 'ignore')
    #
    #             # echo character on UART
    #             self.uart.write(char)
    #
    #             if char == '\r' or char == '\n':
    #                 if self.buffer:
    #                     line = self.buffer
    #                     self.buffer = ""
    #                     self.uart.write('\n')  # new line
    #                     return line
    #                 else:
    #                     self.uart.write('\n')  # on empty enter
    #                     self.uart.write('> ')  #
    #
    #             elif char == '\x7f' or char == '\x08':  # backspace or delete
    #                 if self.buffer:
    #                     self.buffer = self.buffer[:-1]
    #                     # remove character on terminal
    #                     self.uart.write('\b \b')
    #
    #             else:
    #                 self.buffer += char

    def exec(self):
        print('# Welcome to Service Terminal')

        while True:
            line = input('> ').strip()

            # empty line?
            if line == '':
                continue

            cmd = self.parser.parse(line)
            if cmd is None:
                print('Unknown command')
            else:
                cmd.exec()
