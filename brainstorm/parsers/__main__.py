import sys

import click

from . import parse as _parse
from .agent import Agent
from brainstorm.message_queue import MessageQueue


@click.group()
def main():
    pass


@main.command()
@click.argument('parser-name')
@click.argument('raw-data-file', type=click.File('rb'))
def parse(parser_name, raw_data_file, input_topic, output_topic):
    result = _parse(parser_name, raw_data_file.read())
    sys.stdout.write(result.decode())
    sys.stdout.flush()


@main.command()
@click.argument('parser-name')
@click.argument('mq-url')
def run_parser(parser_name, mq_url):
    with MessageQueue(mq_url) as mq:
        Agent.from_parsers_names(mq, [parser_name]).run()


if __name__ == '__main__':
    main(prog_name=__package__)
