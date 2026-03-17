__all__ = ['BaseDevice']


class BaseDevice:
    name = ''
    description = ''

    def __init__(self):
        self.pins = {}

    def capabilities(self):
        return [cls.__name__ for cls in type(self).__bases__
                if cls.__name__.endswith('Mixin')]

    def info(self):
        return {
            'name': self.name,
            'description': self.description,
            'pins': self.pins,
            'capabilities': self.capabilities(),
        }
