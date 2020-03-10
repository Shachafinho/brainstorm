from . import sample_pb2
from .adapter import snapshot_from_protobuf
from .adapter import snapshot_to_protobuf
from .adapter import user_information_from_protobuf
from .adapter import user_information_to_protobuf
from .message import Message, StreamError


def _read_message(input_obj):
    if isinstance(input_obj, bytes):
        return Message.parse(input_obj)
    return Message.parse_stream(input_obj)


def _write_message(data, output_obj=None):
    if output_obj is None:
        return Message.build(data)
    return Message.build_stream(data, output_obj)


class Formatter:
    @staticmethod
    def read_user_information(input_obj):
        user_information = sample_pb2.User()
        try:
            user_information.ParseFromString(_read_message(input_obj))
            return user_information_from_protobuf(user_information)
        except StreamError as e:
            raise EOFError('Failed to read user information') from e

    @staticmethod
    def read_snapshot(input_obj):
        snapshot = sample_pb2.Snapshot()
        try:
            snapshot.ParseFromString(_read_message(input_obj))
            return snapshot_from_protobuf(snapshot)
        except StreamError as e:
            raise EOFError('Failed to read snapshot') from e

    @staticmethod
    def write_user_information(user_information_obj, output_obj=None):
        user_information = user_information_to_protobuf(user_information_obj)
        return _write_message(user_information.SerializeToString(), output_obj)

    @staticmethod
    def write_snapshot(snapshot_obj, output_obj=None):
        snapshot = snapshot_to_protobuf(snapshot_obj)
        return _write_message(snapshot.SerializeToString(), output_obj)


if __name__ == '__main__':
    import contextlib
    import gzip
    read_path = '/home/user/Downloads/sample.mind.gz'
    write_path = '/home/user/Downloads/output.mind.gz.uncompressed'
    with gzip.open(read_path, 'rb') as rf, open(write_path, 'wb') as wf:
        user_information = Formatter.read_user_information(rf)
        print(user_information)
        Formatter.write_user_information(user_information, wf)
        with contextlib.suppress(EOFError):
            snapshot = Formatter.read_snapshot(rf)
            print(snapshot)
            Formatter.write_snapshot(snapshot, wf)
