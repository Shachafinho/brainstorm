import click

import brainstorm.api.config as api_config

from .server import run_server as _run_server


@click.group()
def main():
    pass


@main.command()
@click.option('-h', '--host', type=str, default='127.0.0.1', show_default=True,
              help='GUI Server hostname to listen on')
@click.option('-p', '--port', type=int, default=8080, show_default=True,
              help='GUI Server port to listen on')
@click.option('-H', '--api-host', type=str, default=api_config.DEFAULT_HOST,
              show_default=True, help='API server hostname to listen on')
@click.option('-P', '--api-port', type=int, default=api_config.DEFAULT_PORT,
              show_default=True, help='API server port to listen on')
def run_server(host, port, api_host, api_port):
    _run_server(host, port, api_host, api_port)


if __name__ == '__main__':
    main(prog_name=__package__)
