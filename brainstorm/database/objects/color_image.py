import attr


@attr.s(auto_attribs=True, slots=True)
class ColorImage:
    width: int
    height: int
    data_token: str
