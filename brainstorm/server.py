import pathlib
import threading
import traceback

from brainstorm.context import Context
from brainstorm.parser_manager import ParserManager
from brainstorm.protocol import Hello as HelloMessage
from brainstorm.protocol import Config as ConfigMessage
from brainstorm.protocol import Snapshot as SnapshotMessage
from brainstorm.utils import Listener


PARSERS_DIR = pathlib.Path(__file__).parent.absolute() / 'parsers'


class Handler(threading.Thread):
    def __init__(self, connection, data_dir, parser_manager):
        super().__init__()
        self.conn = connection
        self.data_dir = data_dir
        self.parser_manager = parser_manager

    def _get_hello(self):
        return HelloMessage.deserialize(self.conn.receive_message())

    def _send_config(self):
        config = ConfigMessage(self.parser_manager.parsers_tags)
        self.conn.send_message(config.serialize())

    def _get_snapshot(self):
        return SnapshotMessage.deserialize(self.conn.receive_message())

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

            print('Parsing snapshot...')
            context = Context(self.data_dir, hello.user_id, snapshot.timestamp)
            self.parser_manager.parse(context, snapshot)
        except ConnectionError:
            print(f'Caught exception: {traceback.format_exc()}')


def run_server(address, data_dir):
    ip, port = address
    listener = Listener(port, ip) if ip else Listener(port)
    parser_manager = ParserManager.from_parser_dirs(PARSERS_DIR)

    with listener:
        while True:
            connection = listener.accept()
            handler = Handler(connection, data_dir, parser_manager)
            handler.start()
