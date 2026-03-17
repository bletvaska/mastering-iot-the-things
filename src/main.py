from states.init import Init
from context import Context

if __name__ == "__main__":
    # monkey-patching of builtin open() for reading the Path objects
    import builtins

    _original_open = builtins.open

    def _patched_open(file, *args, **kwargs):
        if not isinstance(file, (str, bytes)):
            file = str(file)
        return _original_open(file, *args, **kwargs)

    builtins.open = _patched_open

    # run
    thsensor = Context(Init)
    thsensor.run()
