import construct

from brainstorm.common.snapshot import Snapshot

from .color_image import ColorImageStruct
from .depth_image import DepthImageStruct
from .feelings import FeelingsStruct
from .rotation import RotationStruct
from .translation import TranslationStruct


_snapshot = construct.Struct(
    'timestamp' / construct.Timestamp(construct.Int64ul, 10 ** -3, 1970),
    'translation' / TranslationStruct,
    'rotation' / RotationStruct,
    'color_image' / ColorImageStruct,
    'depth_image' / DepthImageStruct,
    'feelings' / FeelingsStruct,
).compile()


class SnapshotAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return Snapshot(obj.timestamp, obj.translation, obj.rotation,
                        obj.color_image, obj.depth_image, obj.feelings)

    def _encode(self, obj, context, path):
        return dict(timestamp=obj.timestamp, translation=obj.translation,
                    rotation=obj.rotation, color_image=obj.color_image,
                    depth_image=obj.depth_image, feelings=obj.feelings)


SnapshotStruct = SnapshotAdapter(_snapshot)
