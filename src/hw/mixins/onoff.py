class OnOffMixin:
    def on(self):
        raise NotImplementedError

    def off(self):
        raise NotImplementedError

    def toggle(self):
        raise NotImplementedError