import construct
import contextlib

from brainstorm.snapshot import ColorImage
from brainstorm.snapshot import DepthImage
from brainstorm.snapshot import Feelings
from brainstorm.snapshot import Rotation
from brainstorm.snapshot import Snapshot
from brainstorm.snapshot import Translation
from brainstorm.user_information import UserInformation


USER_INFORMATION = construct.Struct(
    'id' / construct.Int64ul,
    'name' / construct.PascalString(construct.Int32ul, 'utf8'),
    'birth_date' / construct.Timestamp(construct.Int32ul, 1, 1970),
    'gender' / construct.PaddedString(1, 'utf8'),
).compile()


TRANSLATION = construct.Struct(
    'x' / construct.Double,
    'y' / construct.Double,
    'z' / construct.Double,
).compile()


ROTATION = construct.Struct(
    'x' / construct.Double,
    'y' / construct.Double,
    'z' / construct.Double,
    'w' / construct.Double,
).compile()


COLOR_VALUE = construct.Struct(
    'b' / construct.Byte,
    'g' / construct.Byte,
    'r' / construct.Byte,
).compile()


COLOR_IMAGE = construct.Struct(
    'height' / construct.Int32ul,
    'width' / construct.Int32ul,
    'data' / construct.Array(construct.this.width * construct.this.height,
                             COLOR_VALUE),
).compile()


DEPTH_IMAGE = construct.Struct(
    'height' / construct.Int32ul,
    'width' / construct.Int32ul,
    'data' / construct.Array(construct.this.width * construct.this.height,
                             construct.Float32l),
).compile()


FEELINGS = construct.Struct(
    'hunger' / construct.Float32l,
    'thirst' / construct.Float32l,
    'exhaustion' / construct.Float32l,
    'happiness' / construct.Float32l,
).compile()


SNAPSHOT = construct.Struct(
    'timestamp' / construct.Timestamp(construct.Int64ul, 10 ** -3, 1970),
    'translation' / TRANSLATION,
    'rotation' / ROTATION,
    'color_image' / COLOR_IMAGE,
    'depth_image' / DEPTH_IMAGE,
    'feelings' / FEELINGS,
).compile()


def parse_translation(struct):
    return Translation(struct.x, struct.y, struct.z)


def parse_rotation(struct):
    return Rotation(struct.x, struct.y, struct.z, struct.w)


def parse_color_image(struct):
    values = [(d.r, d.g, d.b) for d in struct.data]
    return ColorImage(struct.width, struct.height, values)


def parse_depth_image(struct):
    return DepthImage(struct.width, struct.height, struct.data)


def parse_feelings(struct):
    return Feelings(struct.hunger, struct.thirst,
                    struct.exhaustion, struct.happiness)


class SampleStreamReader:
    def __init__(self, stream):
        self.stream = stream
        self.user_information = self._read_user_information()

    def _read_user_information(self):
        user = USER_INFORMATION.parse_stream(self.stream)
        return UserInformation(user.id, user.name,
                               user.birth_date, user.gender)

    def _read_snapshot(self):
        snapshot = SNAPSHOT.parse_stream(self.stream)
        translation = parse_translation(snapshot.translation)
        rotation = parse_rotation(snapshot.rotation)
        color_image = parse_color_image(snapshot.color_image)
        depth_image = parse_depth_image(snapshot.depth_image)
        feelings = parse_feelings(snapshot.feelings)

        return Snapshot(snapshot.timestamp, translation, rotation,
                        color_image, depth_image, feelings)

    @property
    def snapshots(self):
        with contextlib.suppress(construct.StreamError):
            while True:
                yield self._read_snapshot()


class SampleFileReader:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.stream = open(self.path, 'rb')
        return SampleStreamReader(self.stream)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stream.close()


if __name__ == '__main__':
    path = '/home/user/Downloads/sample.mind'
    with open(path, 'rb') as f:
        reader = SampleStreamReader(f)
        print(reader.user_information)
        for snapshot in reader.snapshots:
            print(snapshot)
