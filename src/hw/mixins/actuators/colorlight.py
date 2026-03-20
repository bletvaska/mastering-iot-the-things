class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)


class ColorlightMixin:
    def color(self, value=None):
        raise NotImplementedError
