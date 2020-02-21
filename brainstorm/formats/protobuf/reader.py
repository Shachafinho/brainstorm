import contextlib

from . import sample_pb2
from .adapter import snapshot_from_protobuf, user_information_from_protobuf
from .message import Message


class Reader:
    def __init__(self, stream):
        self._stream = stream
        self._user_information = None
        self._user_information_end_location = None

    def _read_message(self):
        return Message.parse_stream(self._stream)

    def _read_user_information(self):
        user_information = sample_pb2.User()
        user_information.ParseFromString(self._read_message())
        return user_information_from_protobuf(user_information)

    def _update_user_information(self):
        if not self._user_information:
            self._user_information = self._read_user_information()
            self._user_information_end_location = self._stream.tell()

    @property
    def user_information(self):
        self._update_user_information()
        return self._user_information

    def _read_snapshot(self):
        snapshot = sample_pb2.Snapshot()
        snapshot.ParseFromString(self._read_message())
        return snapshot_from_protobuf(snapshot)

    @property
    def snapshots(self):
        self._update_user_information()
        self._stream.seek(self._user_information_end_location)
        with contextlib.suppress(StopIteration):
            while True:
                yield self._read_snapshot()


if __name__ == '__main__':
    path = '/home/user/Downloads/sample.mind.gz'
    with open(path) as rf:
        reader = Reader(rf)
        print(reader.user_information)
        for snapshot in reader.snapshots:
            print(snapshot)
