class ColorlightMixin:
    def set_color(self, r, g, b):
        raise NotImplementedError

    def color(self):
        raise NotImplementedError