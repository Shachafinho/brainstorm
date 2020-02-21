from .snapshot import SnapshotStruct
from .user_information import UserInformationStruct


class Writer:
    def __init__(self, stream):
        self._stream = stream

    def _write_user_information(self, user_information_obj):
        self._stream.write(UserInformationStruct.build(user_information_obj))

    @property
    def user_information(self):
        pass

    @user_information.setter
    def user_information(self, user_information):
        self._write_user_information(user_information)

    def _write_snapshot(self, snapshot_obj):
        self._stream.write(SnapshotStruct.build(snapshot_obj))

    @property
    def snapshot(self):
        pass

    @snapshot.setter
    def snapshot(self, snapshot):
        self._write_snapshot(snapshot)

    @property
    def snapshots(self):
        pass

    @snapshots.setter
    def snapshots(self, snapshots):
        for snapshot in snapshots:
            self.snapshot = snapshot


if __name__ == '__main__':
    from .reader import Reader
    read_path = '/home/user/Downloads/sample.mind'
    write_path = '/home/user/Downloads/output.mind'
    with open(read_path, 'rb') as rf, open(write_path, 'wb') as wf:
        reader = Reader(rf)
        writer = Writer(wf)

        user_information = reader.user_information
        print(reader.user_information)
        writer.user_information = user_information
        for snapshot in reader.snapshots:
            print(snapshot)
            writer.snapshot = snapshot
