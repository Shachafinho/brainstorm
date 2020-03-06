import click

from . import run_server as _run_server
from brainstorm.message_queue import MessageQueue


@click.group()
def main():
    pass


@main.command()
@click.option('-h', '--host', type=str, default='127.0.0.1', show_default=True,
              help='Server hostname to listen on')
@click.option('-p', '--port', type=int, default=8000, show_default=True,
              help='Server port to listen on')
@click.argument('mq-url')
def run_server(host, port, mq_url):
    with MessageQueue(mq_url) as mq:
        _run_server(host, port, mq.publish)


if __name__ == '__main__':
    main(prog_name=__package__)
