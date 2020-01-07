import construct


class Config:
    class ConfigAdapter(construct.Adapter):
        def _decode(self, obj, context, path):
            return Config(obj)

        def _encode(self, obj, context, path):
            return obj.fields

    ConfigStruct = ConfigAdapter(construct.PrefixedArray(
        construct.Int32ul,
        construct.PascalString(construct.Int32ul, 'utf8')
    ).compile())

    __slots__ = 'fields'

    def __init__(self, fields):
        self.fields = set(fields)

    def __repr__(self):
        return (f'{self.__class__.__name__}(fields={self.fields})')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.fields == other.fields

    def serialize(self):
        return self.ConfigStruct.build(self)

    @classmethod
    def deserialize(cls, data):
        return cls.ConfigStruct.parse(data)
