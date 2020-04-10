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
        data_path = context.path(f'snapshot.{_DEFAULT_FORMAT}')
        with open(data_path, 'wb') as output_file:
            _DEFAULT_FORMATTER.write_snapshot(self.snapshot, output_file)

        return {_TYPE_KEY: str(data_path)}

    @classmethod
    def deserialize(cls, serialized_snapshot):
        data_path = serialized_snapshot[_TYPE_KEY]
        with open(data_path, 'rb') as input_file:
            return cls(_DEFAULT_FORMATTER.read_snapshot(input_file))
