import pathlib

import flask
import pytest

import brainstorm.web


_ADDRESS = '127.0.0.1', 8000
_URL = f'http://{_ADDRESS[0]}:{_ADDRESS[1]}'
_ROOT = pathlib.Path(__file__).absolute().parent.parent / 'brainstorm'
_DATA_DIR = _ROOT.parent / 'data'


@pytest.fixture()
def client():
    webserver = brainstorm.web.create_webserver(_DATA_DIR)
    with webserver.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    for user_dir in _DATA_DIR.iterdir():
        if user_dir.name.startswith('.'):
            continue
        assert f'user {user_dir.name}' in response.data.decode()


def test_user(client):
    for user_dir in _DATA_DIR.iterdir():
        if user_dir.name.startswith('.'):
            continue
        response = client.get(f'/users/{user_dir.name}')
        response_text = response.data.decode()
        assert f'User {user_dir.name}' in response_text
        for thought_file in user_dir.iterdir():
            assert flask.escape(thought_file.read_text()) in response_text
