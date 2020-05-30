import contextlib
import functools

from brainstorm.database import DBError


def _ignore_db_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with contextlib.suppress(DBError):
            return func(*args, **kwargs)
    return wrapper


class Agent:
    """An object responsible for running a saver on some message queue.
    """

    def __init__(self, mq, saver, topics=None):
        """Construct an Agent object.

        Args:
            mq (:class:`~brainstorm.message_queue.MessageQueue`):
              A message queue object to operate on.
            saver (:class:`~brainstorm.saver.Saver`):
              A saver object to be run.
            topics (list(str)): A collection of topics whose results are to be
              saved.
        """
        self._mq = mq
        self._saver = saver
        self._topics = []

        topics = topics or saver.topics
        for topic in topics:
            self.register(topic)

    def register(self, topic):
        """Register a topic of the message queue whose results are to be saved.

        Args:
            topic (str): The topic to be registered.
        """
        bound_saver = functools.partial(self._saver.save, topic)
        self._mq.subscribe(_ignore_db_errors(bound_saver), topic=topic)
        self._topics.append(topic)

    def run(self):
        """Run the saver on all registered topics of the message queue.
        """
        self._mq.consume_forever()
