class BaseCommand:
    """Base class for all service terminal commands.

    Implements the Command design pattern. Each concrete command handles
    a specific terminal instruction identified by its name.

    Commands are registered with a Parser instance and invoked when the
    technician types the corresponding name in the service terminal.

    Example:
        class Blink(BaseCommand):
            name = 'blink'
            description = 'Blinks the diagnostic LED'
            usage = (
                ('blink', 'Blinks the LED once'),
            )

            def __call__(self, params: list) -> None:
                self.context.devices.get(WS2812B).toggle()
    """

    name: str
    description: str
    usage: tuple[str, str] = None

    def __init__(self, context):
        """
        Args:
            context: The shared application context.
        """
        self.context = context

    def __call__(self, params: list):
        """Execute the command.

        Args:
            params: List of string arguments passed to the command.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError()

    def __str__(self):
        """Return a human-readable description or usage information."""
        if self.usage is None:
            return f'{self.name}: {self.description}'
        lines = ['Usage:']
        for option, description in self.usage:
            lines.append(f'  {option:30} {description}')
        return '\n'.join(lines)
