from states.init import Init


class Context:
    def __init__(self):
        self.state = Init(self)

    def change_state(self, state):
        self.state = state

    def run(self):
        self.state.enter()
        while True:
            next_state = self.state.exec()
            if next_state is not self.state:
                self.state.exit()
                self.state = next_state
                self.state.enter()
