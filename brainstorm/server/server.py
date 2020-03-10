import pathlib
import threading
import traceback

from brainstorm.formats import Formatter
from brainstorm.utils import Listener


PARSERS_DIR = pathlib.Path(__file__).parent.parent.absolute() / 'parsers'


class Handler(threading.Thread):
    def __init__(self, connection, publish):
        super().__init__()
        self._conn = connection
        self._publish = publish

    def _get_message(self):
        return self._conn.receive_message()

    def _get_format_tag(self):
        return self._get_message().decode()

    def _get_user_information(self, formatter):
        return formatter.read_user_information(self._get_message())

    def _get_snapshot(self, formatter):
        return formatter.read_snapshot(self._get_message())

    def run(self):
        try:
            print(f'Waiting for format message...')
            format_tag = self._get_format_tag()
            print(f'Got format message: {format_tag!r}')
            formatter = Formatter(format_tag)

            print(f'Waiting for user message...')
            user_information = self._get_user_information(formatter)
            print(f'Got user message: {user_information}')

            print(f'Waiting for snapshot message...')
            snapshot = self._get_snapshot(formatter)
            print(f'Got snapshot message: {snapshot}')

            print('Publishing snapshot...')
            self._publish(str(snapshot))

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
