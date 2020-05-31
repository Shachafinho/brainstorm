import multiprocessing
import pathlib
import socket
import subprocess
import time

import brainstorm.client


_SERVER_ADDRESS = '127.0.0.1', 18000
_SERVER_BACKLOG = 1000
_ROOT = pathlib.Path(__file__).absolute().parent.parent / 'brainstorm'
_DATA_DIR = pathlib.Path(__file__).absolute().parent / 'data'
_SAMPLE_URL = f'protobuf://{str(_DATA_DIR / "example.mind.gz")}'


def test_client():
    server = multiprocessing.Process(target=run_server)
    server.start()
    try:
        time.sleep(0.1)
        host, port = _SERVER_ADDRESS
        base_cmd = ['python', '-m', brainstorm.client.__package__,
                    'upload-sample']
        process = subprocess.Popen(
            base_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _, stderr = process.communicate()
        assert b'usage' in stderr.lower()

        process = subprocess.Popen(
            base_cmd + ['--host', host, '--port', str(port), _SAMPLE_URL],
            stdout=subprocess.PIPE,
        )
        stdout, _ = process.communicate()
        assert b'done' in stdout.lower()
    finally:
        server.terminate()


def run_server():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(_SERVER_ADDRESS)
    server.listen(_SERVER_BACKLOG)
    try:
        while True:
            connection, address = server.accept()
            connection.close()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
