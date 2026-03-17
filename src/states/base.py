class BaseState:
    """Base class for all application states.

    Implements the State design pattern. Each concrete state represents a
    distinct phase of the device lifecycle (e.g. Init, Measurement, Sleep).

    The state machine is driven by the Context, which calls enter(), exec(),
    and exit() at the appropriate times. exec() returns the next state, or
    None to stop the state machine.

    Example:
        class Measurement(BaseState):
            name = 'Measurement'

            def enter(self):
                pass

            def exec(self):
                # perform measurement
                return Sleep(self.context)
    """

    name: str = None

    def __init__(self, context):
        """
        Args:
            context: The shared application context.
        """
        self.context = context
        if self.name is None:
            self.name = self.__class__.__name__

    def enter(self) -> None:
        """Called once when the state machine transitions into this state."""
        pass

    def exec(self):
        """Called repeatedly while this state is active.

        Returns:
            The next state instance, or None to stop the state machine.
        """
        pass

    def exit(self) -> None:
        """Called once when the state machine transitions out of this state."""
        pass
