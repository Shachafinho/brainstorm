import construct


class ColorImage:
    __slots__ = 'width', 'height', 'data'

    def __init__(self, width, height, data):
        self.width = width
        self.height = height
        self.data = data

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'width={self.width}, height={self.height}, '
                f'data=[...])')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.width == other.width and
                self.height == other.height and
                self.data == other.data)


class ColorImageAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        data = [(d.r, d.g, d.b) for d in obj.data]
        return ColorImage(obj.width, obj.height, data)

    def _encode(self, obj, context, path):
        data = (dict(b=d[2], g=d[1], r=d[0]) for d in obj.data)
        return dict(width=obj.width, height=obj.height, data=data)


ColorValue = construct.Struct(
    'b' / construct.Byte,
    'g' / construct.Byte,
    'r' / construct.Byte,
).compile()


ColorImageStruct = ColorImageAdapter(construct.Struct(
    'height' / construct.Int32ul,
    'width' / construct.Int32ul,
    'data' / construct.Array(construct.this.width * construct.this.height,
                             ColorValue),
).compile())
