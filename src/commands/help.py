from .base import BaseCommand


class Help(BaseCommand):
    name = 'help'
    description = 'Show usage of a given command.'
    usage = (
        ('help <cmd>', 'Shows usage for a given command.'),
    )

    def __init__(self, context, commands):
        super().__init__(context)
        self.commands = commands

    def exec(self) -> None:
        if len(self.params) != 1:
            print('Wrong number of parameters.')
            self.show_usage()
            return

        for cmd in self.commands:
            if cmd.name == self.params[0]:
                print(cmd.description)
                if cmd.usage is not None:
                    cmd.show_usage()
                return
        else:
            print('Command not found')
