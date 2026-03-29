class ButtonInterruptMixin:
    def on_press(self, callback) -> None:
        """Register a callback to be called when the button is pressed."""
        raise NotImplementedError

    def on_release(self, callback) -> None:
        """Register a callback to be called when the button is released."""
        raise NotImplementedError
