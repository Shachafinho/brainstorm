import attr

from .rotation import Rotation
from .translation import Translation


@attr.s(auto_attribs=True, slots=True)
class Pose():
    translation: Translation
    rotation: Rotation

