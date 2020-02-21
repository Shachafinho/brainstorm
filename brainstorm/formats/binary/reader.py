import construct
import contextlib

from .snapshot import SnapshotStruct
from .user_information import UserInformationStruct


class Reader:
    def __init__(self, stream):
        self._stream = stream
        self._user_information = None
        self._user_information_end_location = None

    def _read_user_information(self):
        return UserInformationStruct.parse_stream(self._stream)

    def _update_user_information(self):
        if not self._user_information:
            self._user_information = self._read_user_information()
            self._user_information_end_location = self._stream.tell()

    @property
    def user_information(self):
        self._update_user_information()
        return self._user_information

    def _read_snapshot(self):
        return SnapshotStruct.parse_stream(self._stream)

    @property
    def snapshots(self):
        self._update_user_information()
        self._stream.seek(self._user_information_end_location)
        with contextlib.suppress(construct.StreamError):
            while True:
                yield self._read_snapshot()


if __name__ == '__main__':
    path = '/home/user/Downloads/sample.mind'
    with open(path, 'rb') as f:
        reader = Reader(f)
        print(reader.user_information)
        for snapshot in reader.snapshots:
            print(snapshot)
