class BaseState:
    name: str = None

    def __init__(self, context):
        self.context = context
        if self.name is None:
            self.name = self.__class__.__name__

    def enter(self) -> None:
        pass

    def exec(self):
        pass

    def exit(self) -> None:
        pass
