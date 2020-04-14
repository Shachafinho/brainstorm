import attr


@attr.s(auto_attribs=True, slots=True)
class Translation:
    x: float
    y: float
    z: float
