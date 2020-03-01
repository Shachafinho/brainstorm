import pathlib
import threading
import traceback

from brainstorm.protocol import Hello as HelloMessage
from brainstorm.protocol import Config as ConfigMessage
from brainstorm.protocol import Snapshot as SnapshotMessage
from brainstorm.utils import Listener


PARSERS_DIR = pathlib.Path(__file__).parent.parent.absolute() / 'parsers'


class Handler(threading.Thread):
    def __init__(self, connection, publish):
        super().__init__()
        self._conn = connection
        self._publish = publish

    def _get_hello(self):
        return HelloMessage.deserialize(self._conn.receive_message())

    def _send_config(self):
        config = ConfigMessage(SnapshotMessage.__slots__)
        self._conn.send_message(config.serialize())

    def _get_snapshot(self):
        return SnapshotMessage.deserialize(self._conn.receive_message())

    def run(self):
        try:
            print(f'Waiting for hello message...')
            hello = self._get_hello()
            print(f'Got hello message: {hello}')

            print(f'Sending config message...')
            self._send_config()
            print('Done sending config message')

            print(f'Waiting for snapshot message...')
            snapshot = self._get_snapshot()
            print(f'Got snapshot message: {snapshot}')

            print('Publishing snapshot...')
            self._publish(snapshot)

            # context = Context(self.data_dir, hello.user_id, snapshot.timestamp)
            # self.parser_manager.parse(context, snapshot)
        except ConnectionError:
            print(f'Caught exception: {traceback.format_exc()}')


def run_server(host, port, publish):
    listener = Listener(port, host) if host else Listener(port)

    with listener:
        while True:
            connection = listener.accept()
            handler = Handler(connection, publish)
            handler.start()
