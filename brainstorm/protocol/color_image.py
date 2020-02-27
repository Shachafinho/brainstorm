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
                f'data=b\'...\'])')

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
        if not obj:
            return dict(width=0, height=0, data=b'')
        return dict(width=obj.width, height=obj.height, data=obj.data)


ColorImageStruct = ColorImageAdapter(construct.Struct(
    'height' / construct.Int32ul,
    'width' / construct.Int32ul,
    'data' / construct.Bytes(construct.this.width * construct.this.height * 3),
).compile())
