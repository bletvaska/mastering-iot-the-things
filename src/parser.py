from commands.base import BaseCommand


class Parser:
    def __init__(self):
        self.commands = []

    def parse(self, line: str) -> BaseCommand | None:
        line = line.strip()

        name, *params = line.split()
        for cmd in self.commands:
            if cmd.name == name:
                cmd.params = params
                return cmd

        return None

    def register(self, command: BaseCommand):
        self.commands.append(command)
