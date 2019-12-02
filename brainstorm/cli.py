import inspect

import sys


def inspect_function(function):
    argspec = inspect.getfullargspec(function)
    defaults = argspec.defaults or []
    kwonlydefaults = argspec.kwonlydefaults or {}

    # Obtain mandatory arguments.
    positionals = argspec.args[:-len(defaults)] if defaults else argspec.args
    mandatory_keywords = set(argspec.kwonlyargs) - set(kwonlydefaults.keys())
    mandatories = set(positionals) | mandatory_keywords

    # Obtain optional arguments
    optionals = dict(zip(argspec.args[len(positionals):], defaults))
    optionals.update(kwonlydefaults)

    # Check for variable args and kwargs.
    args, kwargs = argspec.varargs, argspec.varkw

    return mandatories, optionals, args, kwargs


class CommandLineInterface:
    def __init__(self, commands=None):
        self.commands = commands or {}

    def command(self, f):
        self.commands[f.__name__] = f
        return f

    def validate_call(self, command_name, command_args):
        command = self.commands[command_name]
        mandatories, optionals, _, kwargs = inspect_function(command)

        # Check for missing mandatory arguments.
        missing_mandatories = mandatories - set(command_args.keys())
        if missing_mandatories:
            raise RuntimeError('Missing mandatory arguments: '
                f'{" ".join(sorted(missing_mandatories))}')

        # Check for any unknown arguments.
        supported_args = set(optionals.keys()) | mandatories
        unknown_args = set(command_args.keys()) - supported_args
        if unknown_args and kwargs is None:
            raise RuntimeError(
                f'Unknown arguments: {" ".join(sorted(unknown_args))}')

    def get_command_usage(self, command_name):
        # Obtain command's mandatory and optional arguments specification.
        command = self.commands[command_name]
        mandatories, optionals, _, kwargs = inspect_function(command)

        # Construct the arguments' representative strings.
        mandatories_str = ' '.join(sorted(mandatories))
        optionals_str = \
            ' '.join([f'[{k}={v}]' for k, v in sorted(optionals.items())])

        # Combine strings to form a usage string.
        usage = command_name
        usage += f' {mandatories_str}' if mandatories_str else ''
        usage += f' {optionals_str}' if optionals_str else ''
        usage += ' [<key>=<value>]*' if kwargs is not None else ''
        return usage

    def main(self):
        usage = f'USAGE: python {sys.argv[0]}'
        # Handle empty or unknown command.
        if len(sys.argv) == 1 or sys.argv[1] not in self.commands:
            usage += ' <command> [<key>=<value>]*'
            if self.commands:
                usage += '\nAvailable commands:\n'
                usage += '\n'.join([f'* {cmd}' for cmd in self.commands])
            print(usage)
            sys.exit(1)

        # Extract the command and its arguments from argv.
        command_name = sys.argv[1]
        try:
            # Parse arguments
            command_args = dict([keyval.split('=') for keyval in sys.argv[2:]])
            # Validate the call.
            self.validate_call(command_name, command_args)
            # Invoke the command.
            self.commands[command_name](**command_args)
        except (RuntimeError, ValueError) as error:
            print(error)
            usage += f' {self.get_command_usage(command_name)}'
            print(usage)
            sys.exit(1)

        sys.exit(0)
