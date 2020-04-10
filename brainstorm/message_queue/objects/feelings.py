import attr


_TYPE_KEY = 'feelings'


@attr.s(auto_attribs=True, slots=True)
class Feelings():
    hunger: float
    thirst: float
    exhaustion: float
    happiness: float

    def serialize(self, context):
        return {_TYPE_KEY: attr.asdict(self)}

    @classmethod
    def deserialize(cls, serialized_feelings):
        return cls(**serialized_feelings[_TYPE_KEY])
