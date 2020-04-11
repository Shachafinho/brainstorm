import io

import arrow
import attr

from brainstorm.common import Snapshot as CommonSnapshot
from brainstorm.formats import Formatter


_DEFAULT_FORMAT = 'protobuf'
_DEFAULT_FORMATTER = Formatter(_DEFAULT_FORMAT)
_TYPE_KEY = 'snapshot'


@attr.s(auto_attribs=True, slots=True)
class Snapshot():
    snapshot: CommonSnapshot

    @property
    def timestamp(self):
        return self.snapshot.timestamp

    @property
    def color_image(self):
        return self.snapshot.color_image

    @property
    def depth_image(self):
        return self.snapshot.depth_image

    @property
    def feelings(self):
        return self.snapshot.feelings

    @property
    def pose(self):
        return self.snapshot.pose

    def serialize(self, context):
        bio = io.BytesIO()
        _DEFAULT_FORMATTER.write_snapshot(self.snapshot, bio)
        data_token = context.save(
            bio.getvalue(), subdir='snapshot', suffix=f'.{_DEFAULT_FORMAT}')
        return {_TYPE_KEY: data_token}

    @classmethod
    def deserialize(cls, context, serialized_snapshot):
        data_token = serialized_snapshot[_TYPE_KEY]
        bio = io.BytesIO(context.load(data_token))
        return cls(_DEFAULT_FORMATTER.read_snapshot(bio))
