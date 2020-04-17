import arrow
import attr


@attr.s(auto_attribs=True, slots=True)
class Snapshot:
    timestamp: arrow.Arrow
