from brainstorm.common import Rotation
from brainstorm.common import Translation
from brainstorm.common import Pose
from brainstorm.utils.serialization import object_to_kwargs


def _serialize_rotation(rotation):
    return {
        'rotation': object_to_kwargs(rotation)
    }


def _deserialize_rotation(rotation_dict):
    return Rotation(**rotation_dict['rotation'])


def _serialize_translation(translation):
    return {
        'translation': object_to_kwargs(translation)
    }


def _deserialize_translation(translation_dict):
    return Translation(**translation_dict['translation'])


def serialize(context, pose):
    return {
        'pose': {
            **_serialize_translation(pose.translation),
            **_serialize_rotation(pose.rotation),
        }
    }


def deserialize(pose_dict):
    return Pose(_deserialize_translation(pose_dict['pose']),
                _deserialize_rotation(pose_dict['pose']))
