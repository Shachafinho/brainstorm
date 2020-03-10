import functools

import click

from . import parse as _parse
from brainstorm.message_queue import MessageQueue


@click.group()
def main():
    pass


@main.command()
@click.argument('parser-name')
@click.argument('raw-data-file', type=click.File('rb'))
def parse(parser_name, raw_data_file):
    _parse(parser_name, raw_data_file.read())


@main.command()
@click.argument('parser-name')
@click.argument('mq-url')
def run_parser(parser_name, mq_url):
    with MessageQueue(mq_url) as mq:
        mq.subscribe(functools.partial(_parse, parser_name))
        mq.consume_forever()


if __name__ == '__main__':
    main(prog_name=__package__)
