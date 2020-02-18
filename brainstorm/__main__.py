import click

from . import run_server
from . import run_webserver
from . import share_mind
from . import Reader


@click.group()
def main():
    pass


@main.group()
def server():
    pass


@server.command()
@click.option('-a', '--address', type=(str, int), default=('0.0.0.0', 5000),
              show_default=True,
              help='Server address of the form: <ip> <port>')
@click.option('-d', '--data-dir', type=str, default='data/',
              show_default=True,
              help='Data directory of uploaded snapshots')
def run(address, data_dir):
    run_server(address, data_dir)


@main.group()
def client():
    pass


@client.command()
@click.option('-a', '--address', type=(str, int), default=('127.0.0.1', 5000),
              show_default=True,
              help='Server address of the form: <ip> <port>')
@click.option('-f', '--mind-file', type=click.Path(exists=True), required=True,
              help='Path to a .mind file to be parsed and sent to the server')
def run(address, mind_file):
    share_mind(address, mind_file)


@main.group()
def web():
    pass


@web.command()
@click.option('-a', '--address', type=(str, int), default=('0.0.0.0', 8000),
              show_default=True,
              help='Server address of the form: <ip> <port>')
@click.option('-d', '--data-dir', type=str, default='data/',
              show_default=True,
              help='Data directory of uploaded snapshots')
def run(address, data_dir):
    run_webserver(address, data_dir)


@main.command()
@click.option('-f', '--snapshot-file', type=str, required=True,
              help='Path to a snapshot file')
def read(snapshot_file):
    with Reader(snapshot_file) as reader:
        print(reader.user_information)
        for snapshot in reader.snapshots:
            print(snapshot)


if __name__ == '__main__':
    main(prog_name=__package__)
