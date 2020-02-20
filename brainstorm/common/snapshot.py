import arrow


class Snapshot:
    __slots__ = 'timestamp', 'translation', 'rotation', 'color_image', \
                'depth_image', 'feelings'

    def __init__(self, timestamp=None, translation=None, rotation=None,
                 color_image=None, depth_image=None, feelings=None):
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
        self.timestamp = timestamp or arrow.utcnow()
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'timestamp={self.timestamp}, translation={self.translation}, '
                f'rotation={self.rotation}, color_image={self.color_image}, '
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
