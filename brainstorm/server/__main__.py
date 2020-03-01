import click

from . import run_server as _run_server


@click.group()
def main():
    pass


@main.command()
@click.option('-h', '--host', type=str, default='127.0.0.1', show_default=True,
              help='Server hostname to listen on')
@click.option('-p', '--port', type=int, default=8000, show_default=True,
              help='Server port to listen on')
@click.argument('mq-url')
def upload_sample(host, port, mq_url):
    _run_server(host, port, mq_url)


if __name__ == '__main__':
    main(prog_name=__package__)
