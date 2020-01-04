import construct


class Hello:
    STRUCT = construct.Struct(
        'id' / construct.Int64ul,
        'name' / construct.PascalString(construct.Int32ul, 'utf8'),
        'birth_date' / construct.Timestamp(construct.Int32ul, 1, 1970),
        'gender' / construct.PaddedString(1, 'utf8'),
    ).compile()

    def __init__(self, user_id, name, birth_date, gender):
        self.user_id = user_id
        self.name = name
        self.birth_date = birth_date
        self.gender = gender

    def serialize(self):
        return self.STRUCT.build(dict(
            id=self.user_id, name=self.name,
            birth_date=self.birth_date, gender=self.gender))

    @classmethod
    def deserialize(cls, data):
        struct = cls.STRUCT.parse(data)
        return cls(struct.id, struct.name, struct.birth_date, struct.gender)


class Config:
    STRUCT = construct.PrefixedArray(
        construct.Int32ul,
        construct.PascalString(construct.Int32ul, 'utf8')
    ).compile()

    def __init__(self, fields):
        self.fields = fields

    def serialize(self):
        return self.STRUCT.build(self.fields)

    @classmethod
    def deserialize(cls, data):
        fields = cls.STRUCT.parse(data)
        return cls(list(fields))


class Snapshot:
    TRANSLATION = construct.Struct(
        'x' / construct.Double,
        'y' / construct.Double,
        'z' / construct.Double,
    ).compile()

    ROTATION = construct.Struct(
        'x' / construct.Double,
        'y' / construct.Double,
        'z' / construct.Double,
        'w' / construct.Double,
    ).compile()

    COLOR_VALUE = construct.Struct(
        'r' / construct.Byte,
        'g' / construct.Byte,
        'b' / construct.Byte,
    ).compile()

    COLOR_IMAGE = construct.Struct(
        'width' / construct.Int32ul,
        'height' / construct.Int32ul,
        'data' / construct.Array(construct.this.width * construct.this.height,
                                 COLOR_VALUE),
    ).compile()

    DEPTH_IMAGE = construct.Struct(
        'width' / construct.Int32ul,
        'height' / construct.Int32ul,
        'data' / construct.Array(construct.this.width * construct.this.height,
                                 construct.Float32l),
    ).compile()

    FEELINGS = construct.Struct(
        'hunger' / construct.Float32l,
        'thirst' / construct.Float32l,
        'exhaustion' / construct.Float32l,
        'happiness' / construct.Float32l,
    ).compile()

    SNAPSHOT = construct.Struct(
        'timestamp' / construct.Timestamp(construct.Int64ul, 10 ** -3, 1970),
        'translation' / TRANSLATION,
        'rotation' / ROTATION,
        'color_image' / COLOR_IMAGE,
        'depth_image' / DEPTH_IMAGE,
        'feelings' / FEELINGS,
    ).compile()

    def __init__(self, timestamp, translation, rotation, color_image,
                 depth_image, feelings):
        self.timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def serialize(self):
        translation = self.TRANSLATION.build(x=self.translation.x)
