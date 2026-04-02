from .base import BaseCommand


class Commands(BaseCommand):
    name = 'commands'
    description = 'Show list of available commands.'

    def __call__(self, params: list) -> None:
        print('List of available commands:')
        for command in self.context.parser:
            print(f'  {command.name:12} {command.description}')
