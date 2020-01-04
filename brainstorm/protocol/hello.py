import construct


class Hello:
    __slots__ = 'user_id', 'name', 'birth_date', 'gender'

    def __init__(self, user_id, name, birth_date, gender):
        self.user_id = user_id
        self.name = name
        self.birth_date = birth_date
        self.gender = gender

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'user_id={self.user_id}, name={self.name}, '
                f'birth_date={self.birth_date}, gender={self.gender})')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.user_id == other.user_id and
                self.name == other.name and
                self.birth_date == other.birth_date and
                self.gender == other.gender)


class HelloAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return Hello(obj.id, obj.name, obj.birth_date, obj.gender)

    def _encode(self, obj, context, path):
        return dict(id=obj.user_id, name=obj.name,
                    birth_date=obj.birth_date, gender=obj.gender)


HelloStruct = HelloAdapter(construct.Struct(
    'id' / construct.Int64ul,
    'name' / construct.PascalString(construct.Int32ul, 'utf8'),
    'birth_date' / construct.Timestamp(construct.Int32ul, 1, 1970),
    'gender' / construct.PaddedString(1, 'utf8'),
).compile())
