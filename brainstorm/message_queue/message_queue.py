import pathlib

import furl.furl as furl

from .topic import Topic
from brainstorm.utils.drivers import DirectoryFocusedConfig
from brainstorm.utils.drivers import FocusedDriverManager


mq_manager = FocusedDriverManager(DirectoryFocusedConfig(
    search_dir=pathlib.Path(__file__).parent.absolute() / 'handlers',
    module_name='handler',
    class_name='Handler',
))


class MessageQueue:
    """A manager object to choose and relay a specific MQ implementation.
    """

    DEFAULT_TOPIC = Topic().name
    """Default topic to publish (consume) messages to (from)."""

    def __init__(self, url):
        """Construct the MessageQueue manager object.

        Args:
            url (str): A URL representing the specific message queue to use.
              The scheme determines the type of the message queue (e.g.
              *rabbitmq*), whereas the host and port determine the address of
              the message queue.
        """
        url = furl(url)
        driver_cls = mq_manager.find_driver(url.scheme)
        self._driver = driver_cls(url)

    def __enter__(self):
        self._driver.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return self._driver.__exit__(exc_type, exc_value, exc_traceback)

    def publish(self, message, topic=None, key=None):
        """Publish a message to the message queue.

        Args:
            message (str): A message to publish to the message queue.
            topic (str): The topic to which the message is published. Defaults
              to :const:`~brainstorm.message_queue.MessageQueue.DEFAULT_TOPIC`.
            key (str): Routing key for the message.
        """
        topic = topic if topic is not None else self.DEFAULT_TOPIC
        self._driver.publish(message, topic, key)

    def subscribe(self, callback, topic=None, key=None):
        """Register a callback to a topic of the message queue.

        Args:
            callback (func(str)): A callback to handle a consumed message.
            topic (str): The topic to which the callback is registered.
              The callback accepts messages consumed from this topic. Defaults
              to :const:`~brainstorm.message_queue.MessageQueue.DEFAULT_TOPIC`.
            key (str): Routing key for the message.
        """
        topic = topic if topic is not None else self.DEFAULT_TOPIC
        self._driver.subscribe(callback, topic, key)

    def consume_forever(self):
        """Consume messages and run registered callbacks indefinitely.
        """
        self._driver.consume_forever()


if __name__ == '__main__':
    import json
    import sys
    import tempfile

    d = {'a': 1, 'b': 2}
    with MessageQueue('rabbitmq://127.0.0.1:5672/') as mq:
        if sys.argv[1].startswith('pub'):
            print(f'Publishing {json.dumps(d)}')
            mq.publish(json.dumps(d))
        elif sys.argv[1].startswith('sub'):
            topic = sys.argv[2] if len(sys.argv) > 2 else None
            def cb(msg):
                with tempfile.NamedTemporaryFile(delete=False) as f:
                    print(f'Consumed msg {msg!r}')
                    print(f'Saving message to file: {f.name}')
                    f.write(msg)
            print(f'Registering consumer on topic {topic!r}')
            mq.subscribe(cb, topic=topic)
            print('Consuming forever!')
            mq.consume_forever()
