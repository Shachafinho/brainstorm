import arrow


class Snapshot:
    __slots__ = 'timestamp', 'pose', 'color_image', \
                'depth_image', 'feelings'

    def __init__(self, timestamp=None, pose=None, color_image=None,
                 depth_image=None, feelings=None):
        '''
        :param timestamp:
        :type timestamp: arrow.Arrow
        :param pose: The user's position in 3D space and head pose.
        :type pose: Pose
        :param color_image:
        :type color_image: ColorImage
        :param depth_image:
        :type depth_image: DepthImage
        :param feelings:
        :type feelings: Feelings
        '''
        self.timestamp = timestamp or arrow.utcnow()
        self.pose = pose
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'timestamp={self.timestamp}, pose={self.pose}, '
                f'color_image={self.color_image}, '
                f'depth_image={self.depth_image}, feelings={self.feelings})')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.timestamp == other.timestamp and
                self.pose == other.pose and
                self.color_image == other.color_image and
                self.depth_image == other.depth_image and
                self.feelings == other.feelings)
