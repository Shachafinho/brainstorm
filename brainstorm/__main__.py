import click

from . import run_server as _run_server
from . import run_webserver as _run_webserver
from . import upload_thought as _upload_thought


@click.group()
def main():
    pass


@main.command()
@click.option('-a', '--address', type=(str, int), default=('0.0.0.0', 5000),
              show_default=True,
              help='Server address of the form: <ip> <port>')
@click.option('-d', '--data-dir', type=str, default='data/',
              show_default=True,
              help='Data directory of uploaded thoughts')
def run_server(address, data_dir):
    _run_server(address, data_dir)


@main.command()
@click.option('-a', '--address', type=(str, int), default=('127.0.0.1', 5000),
              show_default=True,
              help='Server address of the form: <ip> <port>')
@click.option('-u', '--user-id', type=int, required=True,
              help='ID of the thought creator')
@click.option('-t', '--thought', type=str, required=True,
              help='The thought to be uploaded')
def upload_thought(address, user_id, thought):
    _upload_thought(address, user_id, thought)


@main.command()
@click.option('-a', '--address', type=(str, int), default=('0.0.0.0', 8000),
              show_default=True,
              help='Server address of the form: <ip> <port>')
@click.option('-d', '--data-dir', type=str, default='data/',
              show_default=True,
              help='Data directory of uploaded thoughts')
def run_webserver(address, data_dir):
    _run_webserver(address, data_dir)


if __name__ == '__main__':
    main(prog_name=__package__)
