import construct

from brainstorm.common import UserInformation


_user_information = construct.Struct(
    'id' / construct.Int64ul,
    'name' / construct.PascalString(construct.Int32ul, 'utf8'),
    'birth_date' / construct.Timestamp(construct.Int32ul, 1, 1970),
    'gender' / construct.PaddedString(1, 'utf8'),
).compile()


class UserInformationAdapter(construct.Adapter):
    def _decode(self, obj, context, path):
        return UserInformation(obj.id, obj.name, obj.birth_date, obj.gender)

    def _encode(self, obj, context, path):
        return dict(id=obj.user_id, name=obj.name,
                    birth_date=obj.birth_date, gender=obj.gender)


UserInformationStruct = UserInformationAdapter(_user_information)
