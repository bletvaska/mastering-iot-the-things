from .base import BaseCommand


class Commands(BaseCommand):
    name = 'commands'
    description = 'Show list of available commands.'

    def __init__(self, context, commands):
        super().__init__(context)
        self.commands = commands

    def exec(self, params: list) -> None:
        print('List of available commands:')
        for command in self.commands:
            print(f'  {command.name:10} {command.description}')
