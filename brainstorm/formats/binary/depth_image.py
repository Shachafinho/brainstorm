import construct

from brainstorm.common import DepthImage


_depth_image = construct.Struct(
    'height' / construct.Int32ul,
    'width' / construct.Int32ul,
    'data' / construct.Array(construct.this.width * construct.this.height,
                             construct.Float32l),
).compile()


class DepthImageAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return DepthImage(obj.width, obj.height, obj.data)

    def _encode(self, obj, context, path):
        return dict(width=obj.width, height=obj.height, data=obj.data)


DepthImageStruct = DepthImageAdapter(_depth_image)
