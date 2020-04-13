import attr

from .rotation import Rotation
from .translation import Translation


_TYPE_KEY = 'pose'


@attr.s(auto_attribs=True, slots=True)
class Pose():
    translation: Translation
    rotation: Rotation

    def serialize(self, context):
        return {
            _TYPE_KEY: {
                **self.translation.serialize(context),
                **self.rotation.serialize(context)
            }
        }

    @classmethod
    def deserialize(cls, context, serialized_pose):
        rotation = Rotation.deserialize(
            context, serialized_pose[_TYPE_KEY])
        translation = Translation.deserialize(
            context, serialized_pose[_TYPE_KEY])
        return cls(translation, rotation)
