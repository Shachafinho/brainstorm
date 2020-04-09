import functools

import furl.furl as furl
import pika


def callback_wrapper(func):
    @functools.wraps(func)
    def wrapper(ch, method, props, body):
        func(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    return wrapper


class Handler:
    DEFAULT_KEY = '#'

    def __init__(self, url):
        self._connection = None
        self._channel = None

        url = furl(url)
        url.scheme = 'amqp'
        self._connection_params = pika.URLParameters(str(url))

        self._connection = pika.BlockingConnection(self._connection_params)
        self._channel = self._connection.channel()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._connection:
            self._connection.close()

    def publish(self, message, topic=None, key=None):
        key = key or self.DEFAULT_KEY

        self._channel.exchange_declare(
            exchange=topic, exchange_type='topic')
        self._channel.basic_publish(
            exchange=topic, routing_key=key, body=message,
            properties=pika.BasicProperties(delivery_mode=2))

    def subscribe(self, callback, topic=None, key=None):
        key = key or self.DEFAULT_KEY

        result = self._channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        self._channel.exchange_declare(
            exchange=topic, exchange_type='topic')
        self._channel.queue_bind(
            exchange=topic, queue=queue_name, routing_key=key)
        self._channel.basic_consume(
            queue=queue_name, on_message_callback=callback_wrapper(callback))

    def consume_forever(self):
        self._channel.start_consuming()
