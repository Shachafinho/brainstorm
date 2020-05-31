import multiprocessing
import pathlib
import signal
import socket
import subprocess
import threading
import time

import pytest

import brainstorm.server


_SERVER_ADDRESS = '127.0.0.1', 18000
_ROOT = pathlib.Path(__file__).absolute().parent.parent / 'brainstorm'
_MQ_ADDRESS = '127.0.0.1', 15672
_MQ_URL = f'rabbitmq://{_MQ_ADDRESS[0]}:{_MQ_ADDRESS[1]}/'


@pytest.mark.skip
def test_server(mq):
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', '-m', brainstorm.server.__package__, 'run-server',
         '--host', host, '--port', str(port), _MQ_URL],
        stdout=subprocess.PIPE,
    )
    thread = threading.Thread(target=process.communicate)
    thread.start()
    time.sleep(0.5)
    try:
        connection = socket.socket()
        connection.connect(_SERVER_ADDRESS)
        connection.close()
    finally:
        process.send_signal(signal.SIGINT)
        thread.join()
