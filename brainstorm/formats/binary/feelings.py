import construct


class Feelings:
    def __init__(self, hunger, thirst, exhaustion, happiness):
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'hunger={self.hunger}, thirst={self.thirst}, '
                f'exhaustion={self.exhaustion}, happiness={self.happiness})')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.hunger == other.hunger and
                self.thirst == other.thirst and
                self.exhaustion == other.exhaustion and
                self.happiness == other.happiness)


class FeelingsAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return Feelings(obj.hunger, obj.thirst, obj.exhaustion, obj.happiness)

    def _encode(self, obj, context, path):
        return dict(hunger=obj.hunger, thirst=obj.thirst,
                    exhaustion=obj.exhaustion, happiness=obj.happiness)


FeelingsStruct = FeelingsAdapter(construct.Struct(
    'hunger' / construct.Float32l,
    'thirst' / construct.Float32l,
    'exhaustion' / construct.Float32l,
    'happiness' / construct.Float32l,
).compile())
