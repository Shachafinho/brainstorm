import construct


class ColorValueAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return (obj.r, obj.g, obj.b)

    def _encode(self, obj, context, path):
        return dict(zip('rgb', obj))


ColorValueStruct = ColorValueAdapter(construct.Struct(
    'b' / construct.Byte,
    'g' / construct.Byte,
    'r' / construct.Byte,
).compile())


class ColorImage:
    __slots__ = 'width', 'height', 'data'

    def __init__(self, width, height, data):
        self.width = width
        self.height = height
        self.data = data

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'width={self.width}, height={self.height}, '
                f'data=b\'...\')')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.width == other.width and
                self.height == other.height and
                self.data == other.data)


class ColorImageAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return ColorImage(obj.width, obj.height, obj.data)

    def _encode(self, obj, context, path):
        return dict(width=obj.width, height=obj.height, data=obj.data)


ColorImageStruct = ColorImageAdapter(construct.Struct(
    'height' / construct.Int32ul,
    'width' / construct.Int32ul,
    'data' / construct.Array(construct.this.width * construct.this.height,
                             ColorValueStruct),
).compile())
