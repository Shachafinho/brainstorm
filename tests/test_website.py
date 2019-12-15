import multiprocessing
import pathlib

import flask
import pytest
import requests

import brainstorm


_ADDRESS = '127.0.0.1', 8000
_URL = f'http://{_ADDRESS[0]}:{_ADDRESS[1]}'
_ROOT = pathlib.Path(__file__).absolute().parent.parent / 'brainstorm'
_DATA_DIR = _ROOT.parent / 'data'


def run_webserver():
    brainstorm.run_webserver(_ADDRESS, _DATA_DIR)


@pytest.fixture(scope='module')
def webserver():
    process = multiprocessing.Process(target=run_webserver)
    process.start()
    try:
        yield process
    finally:
        process.terminate()


def test_index(webserver):
    response = requests.get(_URL)
    for user_dir in _DATA_DIR.iterdir():
        if user_dir.name.startswith('.'):
            continue
        assert flask.escape(f'user {user_dir.name}') in response.text


def test_user(webserver):
    for user_dir in _DATA_DIR.iterdir():
        if user_dir.name.startswith('.'):
            continue
        response = requests.get(f'{_URL}/users/{user_dir.name}')
        assert flask.escape(f'User {user_dir.name}') in response.text
        for thought_file in user_dir.iterdir():
            assert flask.escape(thought_file.read_text()) in response.text
