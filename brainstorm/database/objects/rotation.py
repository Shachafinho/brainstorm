import attr


@attr.s(auto_attribs=True, slots=True)
class Rotation():
    x: float
    y: float
    z: float
    w: float
