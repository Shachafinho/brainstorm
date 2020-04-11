import arrow
import attr


_TYPE_KEY = 'user_information'


@attr.s(auto_attribs=True, slots=True)
class UserInformation():
    user_id: int
    name: str
    birth_date: arrow.Arrow
    gender: str

    def serialize(self, context):
        return {
            _TYPE_KEY: {
                'user_id': self.user_id,
                'name': self.name,
                'birth_date': self.birth_date.float_timestamp,
                'gender': self.gender,
            }
        }

    @classmethod
    def deserialize(cls, context, serialized_user_information):
        user_dict = serialized_user_information[_TYPE_KEY]
        return cls(
            user_dict['user_id'],
            user_dict['name'],
            arrow.get(user_dict['birth_date']),
            user_dict['gender'],
        )
