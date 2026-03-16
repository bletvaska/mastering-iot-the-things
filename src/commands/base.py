class BaseCommand():
    name: str
    description: str
    usage: tuple[str, str] = None

    def __init__(self, context):
        self.context = context

    def exec(self, params: list):
        raise NotImplementedError()

    def __str__(self):
        if self.usage is None:
            return f'{self.name}: {self.description}'
        lines = ['Usage:']
        for option, description in self.usage:
            lines.append(f'  {option:30} {description}')
        return '\n'.join(lines)
