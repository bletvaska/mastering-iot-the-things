class BaseCommand():
    name: str
    description: str
    usage: str
    params: list[str]

    def __init__(self, context):
        self.params = []
        self.context = context

    def exec(self):
        raise NotImplementedError()

    def show_usage(self):
        print('Usage:\n')

        for option, description in self.usage:
            print(f'  {option:30} {description}')

