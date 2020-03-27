import json
import pathlib

from arrow import Arrow

from .context import Context
from brainstorm.utils.drivers import FocusedDriverManager
from brainstorm.utils.drivers import ModuleFocusedConfig


DEFAULT_NAME = 'snapshot'


topic_manager = FocusedDriverManager(ModuleFocusedConfig(
    search_dir=pathlib.Path(__file__).parent.absolute() / 'topics',
))


def _context_from_mq(context_dict):
    timestamp = Arrow.utcfromtimestamp(context_dict['timestamp']) \
        if 'timestamp' in context_dict else None
    return Context(
        user_id=context_dict['user_id'],
        snapshot_timestamp=timestamp,
        data_dir=context_dict['data_dir'],
    )


def _context_to_mq(context_obj):
    context_dict =  {
        'user_id': context_obj.user_id,
        'data_dir': str(context_obj.data_dir),
    }
    if context_obj.timestamp:
        context_dict['timestamp'] = context_obj.timestamp.float_timestamp

    return context_dict


def _deserialize_data(input_obj):
    if isinstance(input_obj, bytes):
        return json.loads(input_obj)
    return json.load(input_obj)


def _deserialize_message(input_obj):
    message_dict = _deserialize_data(input_obj)
    context = _context_from_mq(message_dict.pop('context'))
    return context, message_dict


def _serialize_data(data_dict, output_obj=None):
    serialized_data = json.dumps(data_dict).encode()
    if output_obj is None:
        return serialized_data
    return output_obj.write(serialized_data)


def _serialize_message(context, obj_dict, output_obj=None):
    return _serialize_data({
        'context': _context_to_mq(context),
        **obj_dict,
    }, output_obj)


class Topic:
    def __init__(self, name=None):
        self._name = name or DEFAULT_NAME
        self._topic = topic_manager.find_driver(self.name)

    @property
    def name(self):
        return self._name

    def serialize(self, context, obj, output_obj=None):
        serialized_obj = self._topic.serialize(context, obj)
        return _serialize_message(context, serialized_obj, output_obj)

    def deserialize(self, message_data):
        context, serialized_obj = _deserialize_message(message_data)
        return context, self._topic.deserialize(serialized_obj)


if __name__ == '__main__':
    topic = Topic('snapshot')
    print(f'topic.name: {topic.name}')

    context = Context(123, Arrow.now())
    snapshot = 'hello'

    print(f'calling topic serialize')
    serialized_snapshot = topic.serialize(context, snapshot)
    print(f'serialized_snapshot: {serialized_snapshot}')

    print(f'calling topic deserialize')
    _, deserialized_snapshot = topic.deserialize(serialized_snapshot)
    print(f'deserialized_snapshot: {deserialized_snapshot}')

    print(f'snapshot == deserialized_snapshot: {snapshot == deserialized_snapshot}')
