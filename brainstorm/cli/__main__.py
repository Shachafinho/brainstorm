import contextlib
import traceback

import click
import requests

import brainstorm.api.config as api_config

from . import urls


def _default_api_options(func):
    func = click.option(
        '-h', '--host', type=str, default=api_config.DEFAULT_HOST,
        show_default=True, help='API server hostname to listen on'
    )(func)
    func = click.option(
        '-p', '--port', type=int, default=api_config.DEFAULT_PORT,
        show_default=True, help='API server port to listen on'
    )(func)
    return func


def _request_data(url):
    response = requests.get(url)
    return response.content.decode()


@contextlib.contextmanager
def _catch_errors_context():
    try:
        yield
    except requests.RequestException as request_error:
        print(f'Caught request error: {request_error}')
    except Exception:
        print(f'Caught unexpected error: {traceback.format_exc()}')


@click.group()
def main():
    pass


@main.command()
@_default_api_options
def get_users(host, port):
    with _catch_errors_context():
        data = _request_data(str(urls.get_users_url(host, port)))
        print(data, end='')


@main.command()
@_default_api_options
@click.argument('user-id')
def get_user(host, port, user_id):
    with _catch_errors_context():
        data = _request_data(str(urls.get_user_url(host, port, user_id)))
        print(data, end='')


@main.command()
@_default_api_options
@click.argument('user-id')
def get_snapshots(host, port, user_id):
    with _catch_errors_context():
        data = _request_data(str(urls.get_snapshots_url(host, port, user_id)))
        print(data, end='')


@main.command()
@_default_api_options
@click.argument('user-id')
@click.argument('snapshot-id')
def get_snapshot(host, port, user_id, snapshot_id):
    with _catch_errors_context():
        data = _request_data(str(urls.get_snapshot_url(
            host, port, user_id, snapshot_id)))
        print(data, end='')


@main.command()
@_default_api_options
@click.argument('user-id')
@click.argument('snapshot-id')
@click.argument('result-name')
@click.option('-s', '--save', 'out_file', type=click.File('w'),
              help='A path to which the result data will be saved')
def get_result(host, port, user_id, snapshot_id, result_name, out_file):
    with _catch_errors_context():
        data = _request_data(str(urls.get_result_url(
            host, port, user_id, snapshot_id, result_name)))
        if out_file:
            out_file.write(data)
        else:
            print(data, end='')


if __name__ == '__main__':
    main(prog_name=__package__)

