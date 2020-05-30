import json
import pathlib

import arrow

from .context import Context
from brainstorm.utils.drivers import FocusedDriverManager
from brainstorm.utils.drivers import ModuleFocusedConfig


topic_manager = FocusedDriverManager(ModuleFocusedConfig(
    search_dir=pathlib.Path(__file__).parent.absolute() / 'topics',
))


def _deserialize_data(input_obj):
    if isinstance(input_obj, bytes):
        return json.loads(input_obj)
    return json.load(input_obj)


def _serialize_data(data_dict, output_obj=None):
    serialized_data = json.dumps(data_dict).encode()
    if output_obj is None:
        return serialized_data
    return output_obj.write(serialized_data)


class Topic:
    """A manager object to choose and relay a specific topic implementation.

    Each topic is responsible for serializing and deserializing the
    :mod:`MQ objects <brainstorm.message_queue.objects>` passing through it.
    """

    DEFAULT_NAME = 'whole_data'
    """Default topic name."""

    def __init__(self, name=None):
        """Construct the Topic manager object.

        Args:
            name (str): The topic name. Defaults to
              :const:`~brainstorm.message_queue.Topic.DEFAULT_NAME`.
        """
        self._name = name or self.DEFAULT_NAME
        self._topic = topic_manager.find_driver(self.name)

    @property
    def name(self):
        """The topic name.

        Return:
            str: The topic name.
        """
        return self._name

    def serialize(self, context, obj, output_obj=None):
        """Serialize the given MQ object using *context* into *output_obj*.

        Args:
            context (:class:`~brainstorm.message_queue.Context`):
              A context object which holds convenient information.
            obj: The MQ object to serialize.
            output_obj: A buffer-like object supporting *write* operations.

        Return:
            If *output_obj* was not specified, return the serialized data.
            Otherwise, return the result of its write function.
        """
        serialized_message = {
            'context': context.serialize(),
            **self._topic.serialize(context, obj),
        }
        return _serialize_data(serialized_message, output_obj)

    def deserialize(self, serialized_data):
        """
        Args:
            serialized_data (bytes or str): The MQ data to deserialize.

        Return:
            tuple(:class:`~brainstorm.message_queue.Context`, object):
              The deserialzed MQ object, together with the context used in its
              serialization.
        """
        serialized_message = _deserialize_data(serialized_data)
        context = Context.deserialize(serialized_message.pop('context'))
        obj = self._topic.deserialize(context, serialized_message)
        return context, obj


if __name__ == '__main__':
    topic = Topic('snapshot')
    print(f'topic.name: {topic.name}')

    context = Context(123, arrow.utcnow())
    snapshot = 'hello'

    print('calling topic serialize')
    serialized_snapshot = topic.serialize(context, snapshot)
    print(f'serialized_snapshot: {serialized_snapshot}')

    print('calling topic deserialize')
    _, deserialized_snapshot = topic.deserialize(serialized_snapshot)
    print(f'deserialized_snapshot: {deserialized_snapshot}')

    print('snapshot == deserialized_snapshot: '
          f'{snapshot == deserialized_snapshot}')
