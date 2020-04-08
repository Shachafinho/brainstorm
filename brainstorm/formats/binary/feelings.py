import construct

from brainstorm.common import Feelings


_feelings = construct.Struct(
    'hunger' / construct.Float32l,
    'thirst' / construct.Float32l,
    'exhaustion' / construct.Float32l,
    'happiness' / construct.Float32l,
).compile()


class FeelingsAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return Feelings(obj.hunger, obj.thirst, obj.exhaustion, obj.happiness)

    def _encode(self, obj, context, path):
        return dict(hunger=obj.hunger, thirst=obj.thirst,
                    exhaustion=obj.exhaustion, happiness=obj.happiness)


FeelingsStruct = FeelingsAdapter(_feelings)
