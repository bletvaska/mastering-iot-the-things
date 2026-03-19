from .base import BaseCommand


class Help(BaseCommand):
    name = 'help'
    description = 'Show usage of a given command.'
    usage = (
        ('help <cmd>', 'Shows usage for a given command.'),
    )

    def __call__(self, params: list) -> None:
        if len(params) != 1:
            print('Wrong number of parameters.')
            print(self)
            return

        for cmd in self.context.parser:
            if cmd.name == params[0]:
                print(cmd)
                break
        else:
            print('Command not found')
