import attr


@attr.s(auto_attribs=True, slots=True)
class Feelings():
    hunger: float
    thirst: float
    exhaustion: float
    happiness: float
