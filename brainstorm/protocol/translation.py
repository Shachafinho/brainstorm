import construct


class Translation:
    __slots__ = 'x', 'y', 'z'

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'x={self.x}, y={self.y}, z={self.z})')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.x == other.x and
                self.y == other.y and
                self.z == other.z)


class TranslationAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return Translation(obj.x, obj.y, obj.z)

    def _encode(self, obj, context, path):
        if not obj:
            return dict(x=0, y=0, z=0)
        return dict(x=obj.x, y=obj.y, z=obj.z)


TranslationStruct = TranslationAdapter(construct.Struct(
    'x' / construct.Double,
    'y' / construct.Double,
    'z' / construct.Double,
).compile())
