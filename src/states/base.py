class BaseState:
    def __init__(self, context):
        self.context = context

    def enter(self) -> None:
        pass

    def exec(self):
        pass

    def exit(self) -> None:
        pass
