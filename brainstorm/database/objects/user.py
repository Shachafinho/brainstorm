import arrow
import attr


@attr.s(auto_attribs=True, slots=True)
class User():
    user_id: int
    name: str
    birthday: arrow.Arrow
    gender: str
