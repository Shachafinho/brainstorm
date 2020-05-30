import click
import traceback

from .client import upload_sample as _upload_sample


@click.group()
def main():
    pass


@main.command()
@click.option('-h', '--host', type=str, default='127.0.0.1', show_default=True,
              help='Server hostname to which the sample is uploaded')
@click.option('-p', '--port', type=int, default=8000, show_default=True,
              help='Server port to which the sample is uploaded')
@click.argument('sample-url')
def upload_sample(host, port, sample_url):
    try:
        _upload_sample(host, port, sample_url)
    except ConnectionError as e:
        print(f'Failed to connect to server: {e}')
    except Exception:
        print(f'Unexpected error: {traceback.format_exc()}')


if __name__ == '__main__':
    main(prog_name=__package__)
