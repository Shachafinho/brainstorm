import construct

from brainstorm.common import Translation


_translation = construct.Struct(
    'x' / construct.Float64l,
    'y' / construct.Float64l,
    'z' / construct.Float64l,
).compile()


class TranslationAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return Translation(obj.x, obj.y, obj.z)

    def _encode(self, obj, context, path):
        return dict(x=obj.x, y=obj.y, z=obj.z)


TranslationStruct = TranslationAdapter(_translation)
