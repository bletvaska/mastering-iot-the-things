class BaseState:
    name: str = ""

    def __init__(self, context):
        self.context = context
        self._name = self.name or self.__class__.__name__

    def enter(self) -> None:
        print(f">> Entering {self._name}")

    def exec(self):
        pass

    def exit(self) -> None:
        print(f">> Leaving {self._name}")
