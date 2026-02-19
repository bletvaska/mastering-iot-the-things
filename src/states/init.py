from .base import BaseState


class Init(BaseState):

    def enter(self):
        print('>> Entering Init State')

    def exec(self):
        print('init')
        return self

    def exit(self):
        print('>> Leaving Init State')
