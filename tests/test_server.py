import pathlib
import signal
import socket
import subprocess
import threading
import time

from brainstorm.__main__ import run_server


_SERVER_ADDRESS = '127.0.0.1', 5000
_ROOT = pathlib.Path(__file__).absolute().parent.parent / 'brainstorm'


def test_server():
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', '-m', _ROOT.name, 'run-server',
         '--address', host, str(port), '--data-dir', 'data/'],
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
