import typing

import arrow
import attr

from brainstorm.utils.converter import converter


@attr.s(auto_attribs=True, slots=True)
class MinimalSnapshot:
    snapshot_id: int
    timestamp: arrow.Arrow

    def serialize(self):
        return converter.unstructure(self)

    @classmethod
    def deserialize(cls, serialized_data):
        return converter.structure(serialized_data, cls)


@attr.s(auto_attribs=True, slots=True)
class Snapshot(MinimalSnapshot):
    results: typing.List[str] = attr.Factory(list)

    def serialize(self):
        return converter.unstructure(self)

    @classmethod
    def deserialize(cls, serialized_data):
        return converter.structure(serialized_data, cls)
