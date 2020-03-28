from brainstorm.common import Feelings
from brainstorm.utils.serialization import object_to_kwargs


def serialize(context, feelings_obj):
    return {'feelings': object_to_kwargs(feelings_obj)}


def deserialize(feelings_dict):
    return Feelings(**feelings_dict['feelings'])
