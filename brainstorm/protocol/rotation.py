import construct


class Rotation:
    __slots__ = 'x', 'y', 'z', 'w'

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'x={self.x}, y={self.y}, z={self.z}, w={self.w})')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.x == other.x and
                self.y == other.y and
                self.z == other.z and
                self.w == other.w)


class RotationAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return Rotation(obj.x, obj.y, obj.z, obj.w)

    def _encode(self, obj, context, path):
        return dict(x=obj.x, y=obj.y, z=obj.z, w=obj.w)


RotationStruct = RotationAdapter(construct.Struct(
    'x' / construct.Double,
    'y' / construct.Double,
    'z' / construct.Double,
    'w' / construct.Double,
).compile())
