import functools

import pika

from furl import furl


def callback_wrapper(func):
    @functools.wraps(func)
    def wrapper(ch, method, props, body):
        func(body, method.routing_key)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    return wrapper


class Handler:
    DEFAULT_EXCHANGE = 'topic_main'
    DEFAULT_KEY = 'snapshot'

    def __init__(self, url):
        self._connection = None
        self._channel = None

        url = furl(url)
        url.scheme = 'amqp'
        self._connection_params = pika.URLParameters(str(url))

    def __enter__(self):
        self._connection = pika.BlockingConnection(self._connection_params)
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange=self.DEFAULT_EXCHANGE, exchange_type='topic')

        return self

    def __exit__(self, exc_type, exc_vaue, exc_traceback):
        self._connection.close()

    def publish(self, message, key=None):
        key = key or self.DEFAULT_KEY
        self._channel.basic_publish(
            exchange=self.DEFAULT_EXCHANGE, routing_key=key, body=message)

    def consume(self, callback, key=None):
        key = key or self.DEFAULT_KEY
        result = self._channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        self._channel.queue_bind(
            exchange=self.DEFAULT_EXCHANGE, queue=queue_name, routing_key=key)
        self._channel.basic_consume(
            queue=queue_name, on_message_callback=callback_wrapper(callback))

    def consume_forever(self):
        self._channel.start_consuming()
