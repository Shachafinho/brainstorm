import contextlib
import functools

from .saver import Saver
from brainstorm.database import DBError


def ignore_db_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with contextlib.suppress(DBError):
            return func(*args, **kwargs)
    return wrapper


class Agent:
    def __init__(self, mq, saver, topics=None):
        self._mq = mq
        self._saver = saver
        self._topics = []

        topics = topics or saver.topics
        for topic in topics:
            self.register(topic)

    def register(self, topic):
        bound_saver = functools.partial(self._saver.save, topic)
        self._mq.subscribe(ignore_db_errors(bound_saver), topic=topic)
        self._topics.append(topic)

    def run(self):
        self._mq.consume_forever()
