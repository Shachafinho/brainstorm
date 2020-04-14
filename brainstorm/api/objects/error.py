import attr

from brainstorm.utils.converter import converter


@attr.s(auto_attribs=True, slots=True)
class Error:
    code: int
    message: str

    def serialize(self):
        return converter.unstructure(self)

    @classmethod
    def deserialize(cls, serialized_data):
        return converter.structure(serialized_data, cls)
