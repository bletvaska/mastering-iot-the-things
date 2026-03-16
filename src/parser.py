from commands.base import BaseCommand


class Parser:
    """
    Service terminal command parser implemented using the Registry design pattern.

    Commands are registered via the `register()` method. The parser then parses
    an input line, looks up the command in the registry and returns it together
    with its parameters.

    Supports iteration over registered commands and the `in` operator for
    checking whether a command exists in the registry.

    Usage:
        parser = Parser()
        parser.register(MyCommand(context))

        result = parser.parse('mycommand arg1 arg2')
        if result:
            cmd, params = result
            cmd.exec(params)

    References:
        https://dev.to/dentedlogic/stop-writing-giant-if-else-chains-master-the-python-registry-pattern-ldm
    """

    def __init__(self):
        self._commands: dict[str, BaseCommand] = {}

    def __contains__(self, key: str) -> bool:
        """Returns True if a command with the given name is registered."""
        return key in self._commands

    def __iter__(self):
        """Iterates over all registered command instances."""
        return iter(self._commands.values())

    def parse(self, line: str) -> tuple | None:
        """
        Parses an input line and returns a (command, params) tuple.

        Returns None if the command is not found in the registry.
        """
        line = line.strip()

        name, *params = line.split()
        if name not in self._commands:
            return None

        return self._commands[name], params

    def register(self, command: BaseCommand):
        """Registers a command into the registry under its name."""
        self._commands[command.name] = command
