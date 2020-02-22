import itertools

import construct

from brainstorm.common.color_image import ColorImage


def grouper(iterable, n, fillvalue=None):
    # Taken from itertools documentation.
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


_color_image = construct.Struct(
    'height' / construct.Int32ul,
    'width' / construct.Int32ul,
    'data' / construct.Bytes(construct.this.width * construct.this.height * 3),
).compile()


class ColorImageAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        rearranged_values = map(reversed, grouper(obj.data, 3))
        data = bytes(itertools.chain.from_iterable(rearranged_values))
        return ColorImage(obj.width, obj.height, data)

    def _encode(self, obj, context, path):
        rearranged_values = map(reversed, grouper(obj.data, 3))
        data = bytes(itertools.chain.from_iterable(rearranged_values))
        return dict(width=obj.width, height=obj.height, data=data)


ColorImageStruct = ColorImageAdapter(_color_image)
