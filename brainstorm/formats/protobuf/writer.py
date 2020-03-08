from .adapter import snapshot_to_protobuf, user_information_to_protobuf
from .message import Message


def _write_message(data, output_obj=None):
    if not output_obj:
        return Message.build(data)
    return Message.build_stream(data, output_obj)


class Writer:
    def __init__(self, stream):
        self._stream = stream

    @property
    def user_information(self):
        pass

    @user_information.setter
    def user_information(self, user_information):
        Writer.write_user_information(user_information, self._stream)

    @property
    def snapshot(self):
        pass

    @snapshot.setter
    def snapshot(self, snapshot):
        Writer.write_snapshot(snapshot, self._stream)

    @property
    def snapshots(self):
        pass

    @snapshots.setter
    def snapshots(self, snapshots):
        for snapshot in snapshots:
            self.snapshot = snapshot

    @staticmethod
    def write_user_information(user_information_obj, output_obj=None):
        user_information = user_information_to_protobuf(user_information_obj)
        return _write_message(user_information.SerializeToString(), output_obj)

    @staticmethod
    def write_snapshot(snapshot_obj, output_obj=None):
        snapshot = snapshot_to_protobuf(snapshot_obj)
        return _write_message(snapshot.SerializeToString(), output_obj)


if __name__ == '__main__':
    from .reader import Reader
    import gzip
    read_path = '/home/user/Downloads/sample.mind.gz'
    write_path = '/home/user/Downloads/output.mind.gz'
    with gzip.open(read_path, 'rb') as rf, open(write_path, 'wb') as wf:
        reader = Reader(rf)
        writer = Writer(wf)
        
        user_information = reader.user_information
        print(reader.user_information)
        writer.user_information = user_information
        for snapshot in reader.snapshots:
            print(snapshot)
            writer.snapshot = snapshot
