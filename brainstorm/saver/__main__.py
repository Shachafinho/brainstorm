import click

from .agent import Agent
from .saver import Saver
from brainstorm.message_queue import MessageQueue


DEFAULT_DB_URL = 'postgresql://127.0.0.1:5432'


@click.group()
def main():
    pass


@main.command()
@click.argument('topic-name')
@click.argument('raw-data-file', type=click.File('rb'))
@click.option('-d', '--database', type=str, default=DEFAULT_DB_URL,
              show_default=True, help='Database URL to save the results to')
def save(topic_name, raw_data_file, database):
    try:
        with Saver(database) as saver:
            saver.save(topic_name, raw_data_file.read())
    except Exception as e:
        print(f'Caught exception: {e}')


@main.command()
@click.argument('db-url')
@click.argument('mq-url')
def run_saver(db_url, mq_url):
    with Saver(db_url) as saver, MessageQueue(mq_url) as mq:
        Agent(mq, saver).run()


if __name__ == '__main__':
    main(prog_name=__package__)
