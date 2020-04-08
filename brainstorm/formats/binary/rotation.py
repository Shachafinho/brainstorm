import construct

from brainstorm.common import Rotation


_rotation = construct.Struct(
    'x' / construct.Float64l,
    'y' / construct.Float64l,
    'z' / construct.Float64l,
    'w' / construct.Float64l,
).compile()


class RotationAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return Rotation(obj.x, obj.y, obj.z, obj.w)

    def _encode(self, obj, context, path):
        return dict(x=obj.x, y=obj.y, z=obj.z, w=obj.w)


RotationStruct = RotationAdapter(_rotation)
