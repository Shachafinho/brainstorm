import attr


_TYPE_KEY = 'rotation'


@attr.s(auto_attribs=True, slots=True)
class Rotation():
    x: float
    y: float
    z: float
    w: float

    def serialize(self, context):
        return {_TYPE_KEY: attr.asdict(self)}

    @classmethod
    def deserialize(cls, context, serialized_rotation):
        return cls(**serialized_rotation[_TYPE_KEY])
