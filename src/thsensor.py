from states.init import Init


class THSensor:
    def __init__(self):
        self.state = Init(self)

    def change_state(self, state):
        self.state = state

    def run(self):
        while True:
            current_state = self.state

            current_state.enter()
            self.state = current_state.exec()
            current_state.exit()
