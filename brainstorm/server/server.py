import pathlib
import threading
import traceback

from brainstorm.formats import Formatter
from brainstorm.message_queue import Context
from brainstorm.message_queue import Topic
from brainstorm.utils import Listener


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

    def _publish_user_information_message(self, user_information):
        user_context = Context(user_information.user_id)
        user_message = Topic('user_information').serialize(
            user_context, user_information)
        print(f'Publishing user information message: {user_message}...')
        self._publish(user_message)
        print('Done publishing user information message')

    def _publish_snapshot_message(self, user_id, snapshot):
        snapshot_context = Context(user_id, snapshot.timestamp)
        snapshot_message = Topic('snapshot').serialize(
            snapshot_context, snapshot)
        print(f'Publishing snapshot message: {snapshot_message}...')
        self._publish(snapshot_message)
        print('Done publishing snapshot message')

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

            # self._publish_user_information_message(user_information)
            self._publish_snapshot_message(user_information.user_id, snapshot)

        except ConnectionError:
            print(f'Client disconnected')
        except Exception:
            print(f'Unexpected error: {traceback.format_exc()}')


def run_server(host, port, publish):
    listener = Listener(port, host) if host else Listener(port)

    with listener:
        while True:
            connection = listener.accept()
            handler = Handler(connection, publish)
            handler.start()
