class BaseCommand():
    name: str
    description: str
    usage: tuple[str, str] = None
    params: list[str]

    def __init__(self, context):
        self.params = []
        self.context = context

    def exec(self):
        raise NotImplementedError()

    def __str__(self):
        if self.usage is None:
            return f'{self.name}: {self.description}'
        lines = ['Usage:']
        for option, description in self.usage:
            lines.append(f'  {option:30} {description}')
        return '\n'.join(lines)
