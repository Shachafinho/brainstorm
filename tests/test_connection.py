import socket
import time

import pytest

from brainstorm.utils import Connection


_PORT = 1234
_DATA = b'Hello, world!'


@pytest.fixture
def server():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', _PORT))
    server.listen(1000)
    try:
        time.sleep(0.1)
        yield server
    finally:
        server.close()


def read_from_sock(sock):
    chunks = []
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)
    return b''.join(chunks)


def test_close(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    assert not sock._closed
    connection.close()
    assert sock._closed


def test_context_manager(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    with connection:
        assert not sock._closed
    assert sock._closed


def test_connect(server):
    with Connection.connect('127.0.0.1', _PORT):
        server.accept()


def test_repr(server):
    with Connection.connect('127.0.0.1', _PORT) as connection:
        _, other_port = connection.socket.getsockname()
        assert repr(connection) == \
            f'<Connection from 127.0.0.1:{other_port} to 127.0.0.1:{_PORT}>'


def test_send(server):
    with Connection.connect('127.0.0.1', _PORT) as connection:
        client, _ = server.accept()
        connection.send(_DATA)

    assert read_from_sock(client) == _DATA


def test_send_message(server):
    with Connection.connect('127.0.0.1', _PORT) as connection:
        client, _ = server.accept()
        connection.send_message(_DATA)

    received_bytes = read_from_sock(client)
    assert int.from_bytes(received_bytes[:4], 'little') == len(_DATA)
    assert received_bytes[4:] == _DATA


def test_receive(server):
    with Connection.connect('127.0.0.1', _PORT) as connection:
        client, _ = server.accept()
        client.sendall(_DATA)
        first = connection.receive(1)
        assert first == _DATA[:1]
        rest = connection.receive(len(_DATA) - 1)
        assert rest == _DATA[1:]


def test_receive_message(server):
    with Connection.connect('127.0.0.1', _PORT) as connection:
        client, _ = server.accept()
        client.sendall(len(_DATA).to_bytes(4, 'little'))
        client.sendall(_DATA)
        message_bytes = connection.receive_message()
        assert message_bytes == _DATA


def test_incomplete_data(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    try:
        client, _ = server.accept()
        client.sendall(b'1')
        client.close()
        with pytest.raises(Exception):
            connection.receive(2)
    finally:
        connection.close()
