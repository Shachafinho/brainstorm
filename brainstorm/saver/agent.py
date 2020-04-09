import functools

from .saver import Saver


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
        self._mq.subscribe(bound_saver, topic=topic)
        self._topics.append(topic)

    def run(self):
        self._mq.consume_forever()
