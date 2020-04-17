import attr

from .rotation import Rotation
from .translation import Translation
from brainstorm.utils.converter import converter


@attr.s(auto_attribs=True, slots=True)
class Pose:
    translation: Translation
    rotation: Rotation

    def serialize(self):
        return converter.unstructure(self)

    @classmethod
    def deserialize(cls, serialized_data):
        return converter.structure(serialized_data, cls)
