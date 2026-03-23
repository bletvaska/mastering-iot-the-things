from .base import BaseState
from .sleep import Sleep


class Error(BaseState):
    name = 'Error'

    def __init__(self, context, exception, **kwargs):
        super().__init__(context)
        self.exception = exception

    def exec(self):
        print('Houston, we have problem.')

        return Sleep(self.context)
