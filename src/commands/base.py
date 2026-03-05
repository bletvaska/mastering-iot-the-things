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