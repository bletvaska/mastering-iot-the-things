class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)


class ColorlightMixin:
    def set_color(self, r, g, b):
        raise NotImplementedError

    def color(self):
        raise NotImplementedError
