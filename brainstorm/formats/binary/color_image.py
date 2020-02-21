import construct

from brainstorm.common.color_image import ColorImage


_color_value = construct.Struct(
    'b' / construct.Byte,
    'g' / construct.Byte,
    'r' / construct.Byte,
).compile()


class ColorValueAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return (obj.r, obj.g, obj.b)

    def _encode(self, obj, context, path):
        return dict(zip('rgb', obj))


ColorValueStruct = ColorValueAdapter(_color_value)


_color_image = construct.Struct(
    'height' / construct.Int32ul,
    'width' / construct.Int32ul,
    'data' / construct.Array(construct.this.width * construct.this.height,
                             ColorValueStruct),
).compile()


class ColorImageAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return ColorImage(obj.width, obj.height, obj.data)

    def _encode(self, obj, context, path):
        return dict(width=obj.width, height=obj.height, data=obj.data)


ColorImageStruct = ColorImageAdapter(_color_image)
