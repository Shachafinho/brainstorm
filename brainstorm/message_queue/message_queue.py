import pathlib

from furl import furl

from brainstorm.utils.drivers import FocusedConfig
from brainstorm.utils.drivers import FocusedDriverManager


mq_manager = FocusedDriverManager(FocusedConfig(
    search_dir=pathlib.Path(__file__).parent.absolute(),
    module_name='handler',
    class_name='Handler',
))


class MessageQueue:
    def __init__(self, url):
        url = furl(url)
        driver_cls = mq_manager.find_driver(url.scheme)
        self._driver = driver_cls(url)

    def __enter__(self):
        self._driver.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return self._driver.__exit__(exc_type, exc_value, exc_traceback)

    def publish(self, message, topic=None, key=None):
        self._driver.publish(message, topic, key)

    def subscribe(self, callback, topic=None, key=None):
        self._driver.subscribe(callback, topic, key)

    def consume_forever(self):
        self._driver.consume_forever()


if __name__ == '__main__':
    import json
    import sys

    d = {'a': 1, 'b': 2}
    with MessageQueue('rabbitmq://127.0.0.1:5672/') as mq:
        if sys.argv[1].startswith('pub'):
            print(f'Publishing {json.dumps(d)}')
            mq.publish(json.dumps(d))
        elif sys.argv[1].startswith('sub'):
            def cb(msg, key):
                print(f'Consumed msg {msg!r} using routing key: {key!r}')
            print('Registering consumer')
            mq.subscribe(cb)
            print('Consuming forever!')
            mq.consume_forever()
