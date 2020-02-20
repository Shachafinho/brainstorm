from .adapter import snapshot_to_protobuf, user_information_to_protobuf
from .message import Message


class ProtobufStreamWriter:
    def __init__(self, stream):
        self._stream = stream

    def _write_message(self, data):
        self._stream.write(Message.build(data))

    def _write_user_information(self, user_information_obj):
        user_information = user_information_to_protobuf(user_information_obj)
        self._write_message(user_information.SerializeToString())

    @property
    def user_information(self):
        pass

    @user_information.setter
    def user_information(self, user_information):
        self._write_user_information(user_information)

    def _write_snapshot(self, snapshot_obj):
        snapshot = snapshot_to_protobuf(snapshot_obj)
        self._write_message(snapshot.SerializeToString)

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
    from .reader import ProtobufStreamReader
    import gzip
    read_path = '/home/user/Downloads/sample.mind.gz'
    write_path = '/home/user/Downloads/output.mind.gz'
    with gzip.open(read_path, 'rb') as rf, gzip.open(write_path, 'wb') as wf:
        with ProtobufStreamReader(rf) as reader, \
             ProtobufStreamWriter(wf) as writer:
            user_information = reader.user_information
            print(reader.user_information)
            writer.user_information = user_information
            for snapshot in reader.snapshots:
                print(snapshot)
                writer.snapshot = snapshot
