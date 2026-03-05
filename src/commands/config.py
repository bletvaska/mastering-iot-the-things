from commands.base import BaseCommand


class Config(BaseCommand):
    name = 'config'
    description = 'Configuration Management.'
    usage = ('Usage:\n'
             '  config show                shows configuration\n'
             '  config set <key> <value>   sets configuration key\n'
             '  config get <key>           gets configuration value\n'
             )

    def exec(self) -> None:
        if len(self.params) == 0:
            print(self.usage)
            return

        cmd = self.params[0].lower()


