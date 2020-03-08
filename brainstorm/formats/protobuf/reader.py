import contextlib

from . import sample_pb2
from .adapter import snapshot_from_protobuf, user_information_from_protobuf
from .message import Message, StreamError


def _read_message(input_obj):
    if isinstance(input_obj, bytes):
        return Message.parse(input_obj)
    return Message.parse_stream(input_obj)


class Reader:
    def __init__(self, stream):
        self._stream = stream
        self._user_information = None
        self._user_information_end_location = None

    def _update_user_information(self):
        if not self._user_information:
            self._user_information = Reader.read_user_information(self._stream)
            self._user_information_end_location = self._stream.tell()

    @property
    def user_information(self):
        self._update_user_information()
        return self._user_information

    @property
    def snapshots(self):
        self._update_user_information()
        self._stream.seek(self._user_information_end_location)
        with contextlib.suppress(StreamError):
            while True:
                yield Reader.read_snapshot(self._stream)

    @staticmethod
    def read_user_information(input_obj):
        user_information = sample_pb2.User()
        user_information.ParseFromString(_read_message(input_obj))
        return user_information_from_protobuf(user_information)

    @staticmethod
    def read_snapshot(input_obj):
        snapshot = sample_pb2.Snapshot()
        snapshot.ParseFromString(_read_message(input_obj))
        return snapshot_from_protobuf(snapshot)


if __name__ == '__main__':
    path = '/home/user/Downloads/sample.mind.gz'
    import gzip
    with gzip.open(path) as rf:
        reader = Reader(rf)
        print(reader.user_information)
        for snapshot in reader.snapshots:
            print(snapshot)
