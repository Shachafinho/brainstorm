import construct

from brainstorm.common import Pose

from .rotation import RotationStruct
from .translation import TranslationStruct


_pose = construct.Struct(
    'translation' / TranslationStruct,
    'rotation' / RotationStruct,
).compile()


class PoseAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return Pose(obj.translation, obj.rotation)

    def _encode(self, obj, context, path):
        return dict(translation=obj.translation, rotation=obj.rotation)


PoseStruct = PoseAdapter(_pose)
