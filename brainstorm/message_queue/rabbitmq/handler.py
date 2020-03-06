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

        self._connection = pika.BlockingConnection(self._connection_params)
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange=self.DEFAULT_EXCHANGE, exchange_type='topic')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_vaue, exc_traceback):
        if self._connection:
            self._connection.close()

    def publish(self, message, topic=None, key=None):
        exchange = topic or self.DEFAULT_EXCHANGE
        key = key or self.DEFAULT_KEY

        self._channel.basic_publish(
            exchange=exchange, routing_key=key, body=message,
            properties=pika.BasicProperties(delivery_mode=2))

    def subscribe(self, callback, topic=None, key=None):
        exchange = topic or self.DEFAULT_EXCHANGE
        key = key or self.DEFAULT_KEY

        result = self._channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        self._channel.queue_bind(
            exchange=exchange, queue=queue_name, routing_key=key)
        self._channel.basic_consume(
            queue=queue_name, on_message_callback=callback_wrapper(callback))

    def consume_forever(self):
        self._channel.start_consuming()
