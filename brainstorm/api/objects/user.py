import arrow
import attr

from brainstorm.utils.converter import converter


@attr.s(auto_attribs=True, slots=True)
class MinimalUser:
    user_id: int
    name: str

    def serialize(self):
        return converter.unstructure(self)

    @classmethod
    def deserialize(cls, serialized_data):
        return converter.structure(serialized_data, cls)


@attr.s(auto_attribs=True, slots=True)
class User(MinimalUser):
    birthday: arrow.Arrow
    gender: str

    def serialize(self):
        return converter.unstructure(self)

    @classmethod
    def deserialize(cls, serialized_data):
        return converter.structure(serialized_data, cls)
