import construct

from brainstorm.common import Snapshot

from .color_image import ColorImageStruct
from .depth_image import DepthImageStruct
from .feelings import FeelingsStruct
from .pose import PoseStruct


_snapshot = construct.Struct(
    'timestamp' / construct.Timestamp(construct.Int64ul, 10 ** -3, 1970),
    'pose' / PoseStruct
    'color_image' / ColorImageStruct,
    'depth_image' / DepthImageStruct,
    'feelings' / FeelingsStruct,
).compile()


class SnapshotAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return Snapshot(obj.timestamp, obj.pose obj.color_image,
                        obj.depth_image, obj.feelings)

    def _encode(self, obj, context, path):
        return dict(timestamp=obj.timestamp, pose=obj.pose,
                    color_image=obj.color_image, depth_image=obj.depth_image,
                    feelings=obj.feelings)


SnapshotStruct = SnapshotAdapter(_snapshot)
