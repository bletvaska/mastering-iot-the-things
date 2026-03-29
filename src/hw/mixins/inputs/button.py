class ButtonMixin:
    def is_pressed(self) -> bool:
        """Return True if the button is currently pressed."""
        raise NotImplementedError
