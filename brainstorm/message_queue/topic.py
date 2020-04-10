import json
import pathlib

import arrow

from .context import Context
from brainstorm.utils.drivers import FocusedDriverManager
from brainstorm.utils.drivers import ModuleFocusedConfig


DEFAULT_NAME = 'whole_data'


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
    def __init__(self, name=None):
        self._name = name or DEFAULT_NAME
        self._topic = topic_manager.find_driver(self.name)

    @property
    def name(self):
        return self._name

    def serialize(self, context, obj, output_obj=None):
        serialized_message = {
            'context': context.serialize(),
            **self._topic.serialize(context, obj),
        }
        return _serialize_data(serialized_message, output_obj)

    def deserialize(self, serialized_data):
        serialized_message = _deserialize_data(serialized_data)
        context = Context.deserialize(serialized_message.pop('context'))
        obj = self._topic.deserialize(serialized_message)
        return context, obj


if __name__ == '__main__':
    topic = Topic('snapshot')
    print(f'topic.name: {topic.name}')

    context = Context(123, arrow.utcnow())
    snapshot = 'hello'

    print(f'calling topic serialize')
    serialized_snapshot = topic.serialize(context, snapshot)
    print(f'serialized_snapshot: {serialized_snapshot}')

    print(f'calling topic deserialize')
    _, deserialized_snapshot = topic.deserialize(serialized_snapshot)
    print(f'deserialized_snapshot: {deserialized_snapshot}')

    print(f'snapshot == deserialized_snapshot: {snapshot == deserialized_snapshot}')
