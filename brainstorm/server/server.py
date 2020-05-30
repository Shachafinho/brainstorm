import threading
import traceback

from brainstorm.formats import Formatter
from brainstorm.message_queue import Context
from brainstorm.message_queue import Topic
from brainstorm.message_queue.objects import Snapshot as MQSnapshot
from brainstorm.message_queue.objects import UserInformation as MQUser
from brainstorm.message_queue.objects import WholeData as MQWholeData
from brainstorm.utils import Listener


class Handler(threading.Thread):
    def __init__(self, connection, publish):
        """Construct a server handler.

        Args:
            connection (:class:`~brainstorm.utils.connection.Connection`):
              A connection object to communicate with the associated client.
            publish (func(str)): Function which accepts a message (str) and
              publishes it to a message queue.
        """
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

    def _publish_whole_data_message(self, user_information, snapshot):
        mq_user = MQUser(user_information.user_id, user_information.name,
                         user_information.birth_date, user_information.gender)
        mq_snapshot = MQSnapshot(snapshot)
        mq_whole_data = MQWholeData(mq_user, mq_snapshot)
        whole_data_message = Topic('whole_data').serialize(
            Context(), mq_whole_data)
        print(f'Publishing whole data message: {whole_data_message}...')
        self._publish(whole_data_message)
        print('Done publishing whole data message')

    def run(self):
        """Receive a sample and publish it to the message queue.

        First, receive the format in which the sample is received.
        Then, receive the sample's user information, followed by a snapshot.

        Once the entire sample is received, publish both user and snapshot
        information to the message queue.
        """
        try:
            print('Waiting for format message...')
            format_tag = self._get_format_tag()
            print(f'Got format message: {format_tag!r}')
            formatter = Formatter(format_tag)

            print('Waiting for user message...')
            user_information = self._get_user_information(formatter)
            print(f'Got user message: {user_information}')

            print('Waiting for snapshot message...')
            snapshot = self._get_snapshot(formatter)
            print(f'Got snapshot message: {snapshot}')

            self._publish_whole_data_message(user_information, snapshot)

        except ConnectionError:
            print('Client disconnected')
        except Exception:
            print(f'Unexpected error: {traceback.format_exc()}')


def run_server(host, port, publish):
    """Run a server to receive samples and publish them to a message queue.

    The server listens on the specified host and port, and awaits a connection.

    Once a connection is accepted, the server receives samples and then
    publishes them to the message queue using the specified publish function.

    Args:
        host (str): Server hostname to listen on.
        port (int): Server port to listen on.
        publish (func(str)): Function which accepts a message (str) and
          publishes it to a message queue.
    """
    listener = Listener(port, host) if host else Listener(port)

    with listener:
        while True:
            connection = listener.accept()
            handler = Handler(connection, publish)
            handler.start()
