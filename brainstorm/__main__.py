from . import run_server as _run_server
from . import run_webserver as _run_webserver
from . import upload_thought as _upload_thought
from .cli import CommandLineInterface


cli = CommandLineInterface()


@cli.command
def run_server(address, data):
    if ':' in address:
        ip, port = address.split(':')
    else:
        # Assume the supplied address consists of port only.
        ip, port = None, address

    _run_server((ip, int(port)), data)


@cli.command
def upload_thought(address, user, thought):
    ip, port = address.split(':')
    user_id = int(user)

    _upload_thought((ip, int(port)), user_id, thought)


@cli.command
def run_webserver(address, data_dir):
    _run_webserver(address, data_dir)


if __name__ == '__main__':
    cli.main()
