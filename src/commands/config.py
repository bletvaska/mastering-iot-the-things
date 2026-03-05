from commands.base import BaseCommand


class Config(BaseCommand):
    name = 'config'
    description = 'Configuration Management.'
    usage = (
        ('config show', 'shows configuration'),
        ('config set <key> <value>', 'sets configuration key'),
        ('config get <key>', 'gets configuration value'),
    )

    def exec(self) -> None:
        if len(self.params) == 0:
            print(self.usage)
            return

        cmd = self.params[0].lower()
