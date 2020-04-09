import attr


@attr.s(auto_attribs=True, slots=True)
class DepthImage():
    width: int
    height: int
    data_path: str
