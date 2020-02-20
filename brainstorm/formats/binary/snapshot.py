import construct

from .color_image import ColorImageStruct
from .depth_image import DepthImageStruct
from .feelings import FeelingsStruct
from .rotation import RotationStruct
from .translation import TranslationStruct


class Snapshot:
    __slots__ = ('timestamp', 'translation', 'rotation', 'color_image',
                 'depth_image', 'feelings')

    def __init__(self, timestamp, translation, rotation, color_image,
                 depth_image, feelings):
        '''
        :param timestamp:
        :type timestamp: arrow.Arrow
        :param translation: The user's position in 3D space.
        :type translation: tuple(double, double, double)
        :param rotation: The pose of the user's head.
        :type rotation: tuple(double, double, double, double)
        :param color_image:
        :type color_image: ColorImage
        :param depth_image:
        :type depth_image: DepthImage
        :param feelings:
        :type feelings: Feelings
        '''
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'timestamp={self.timestamp}, rotation={self.rotation}, '
                f'color_image={self.color_image}, '
                f'depth_image={self.depth_image}, feelings={self.feelings})')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.timestamp == other.timestamp and
                self.translation == other.translation and
                self.rotation == other.rotation and
                self.color_image == other.color_image and
                self.depth_image == other.depth_image and
                self.feelings == other.feelings)


class SnapshotAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return Snapshot(obj.timestamp, obj.translation, obj.rotation,
                        obj.color_image, obj.depth_image, obj.feelings)

    def _encode(self, obj, context, path):
        return dict(timestamp=obj.timestamp, translation=obj.translation,
                    rotation=obj.rotation, color_image=obj.color_image,
                    depth_image=obj.depth_image, feelings=obj.feelings)


SnapshotStruct = SnapshotAdapter(construct.Struct(
    'timestamp' / construct.Timestamp(construct.Int64ul, 10 ** -3, 1970),
    'translation' / TranslationStruct,
    'rotation' / RotationStruct,
    'color_image' / ColorImageStruct,
    'depth_image' / DepthImageStruct,
    'feelings' / FeelingsStruct,
).compile())
