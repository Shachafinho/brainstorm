import click

from . import config
from .server import run_api_server


DEFAULT_DB_URL = 'postgresql://127.0.0.1:5432'


@click.group()
def main():
    pass


@main.command()
@click.option('-h', '--host', type=str, default=config.DEFAULT_HOST,
              show_default=True, help='API server hostname to listen on')
@click.option('-p', '--port', type=int, default=config.DEFAULT_PORT,
              show_default=True, help='API server port to listen on')
@click.option('-d', '--database', type=str, default=DEFAULT_DB_URL,
              show_default=True, help='Database URL to get the data from')
def run_server(host, port, database):
    run_api_server(host, port, database)


if __name__ == '__main__':
    main(prog_name=__package__)

