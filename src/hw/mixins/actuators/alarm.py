class AlarmMixin:
    def set_alarm(self, nr: int = 0, *params):
        raise NotImplementedError()

    def clear_alarm(self, nr: int = 0):
        raise NotImplementedError()
