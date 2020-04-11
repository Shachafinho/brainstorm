import attr


_TYPE_KEY = 'translation'


@attr.s(auto_attribs=True, slots=True)
class Translation():
    x: float
    y: float
    z: float

    def serialize(self, context):
        return {_TYPE_KEY: attr.asdict(self)}

    @classmethod
    def deserialize(cls, context, serialized_translation):
        return cls(**serialized_translation[_TYPE_KEY])
