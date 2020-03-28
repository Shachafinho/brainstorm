from brainstorm.common import Rotation
from brainstorm.common import Translation
from brainstorm.utils.serialization import object_to_kwargs


def serialize(context, pose):
    translation, rotation = pose
    return {
        'pose': {
            'translation': object_to_kwargs(translation),
            'rotation': object_to_kwargs(rotation),
        }
    }


def deserialize(pose_dict):
    translation_kwargs = pose_dict['pose']['translation']
    rotation_kwargs = pose_dict['pose']['rotation']
    return Translation(**translation_kwargs), Rotation(**rotation_kwargs)
