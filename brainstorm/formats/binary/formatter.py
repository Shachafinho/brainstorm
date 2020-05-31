import construct

from .snapshot import SnapshotStruct
from .user_information import UserInformationStruct


class Formatter:
    @staticmethod
    def read_user_information(input_obj):
        try:
            if isinstance(input_obj, bytes):
                return UserInformationStruct.parse(input_obj)
            return UserInformationStruct.parse_stream(input_obj)
        except construct.StreamError as e:
            raise EOFError('Failed to read user information') from e

    @staticmethod
    def read_snapshot(input_obj):
        try:
            if isinstance(input_obj, bytes):
                return SnapshotStruct.parse(input_obj)
            return SnapshotStruct.parse_stream(input_obj)
        except construct.StreamError as e:
            raise EOFError('Failed to read snapshot') from e

    @staticmethod
    def write_user_information(user_information_obj, output_obj=None):
        if output_obj is None:
            return UserInformationStruct.build(user_information_obj)
        return UserInformationStruct.build_stream(
            user_information_obj, output_obj)

    @staticmethod
    def write_snapshot(snapshot_obj, output_obj=None):
        if output_obj is None:
            return SnapshotStruct.build(snapshot_obj)
        return SnapshotStruct.build_stream(snapshot_obj, output_obj)


if __name__ == '__main__':
    import contextlib
    read_path = '/home/user/Downloads/sample.mind'
    write_path = '/home/user/Downloads/output.mind'
    with open(read_path, 'rb') as rf, open(write_path, 'wb') as wf:
        user_information = Formatter.read_user_information(rf)
        print(user_information)
        Formatter.write_user_information(user_information, wf)
        with contextlib.suppress(EOFError):
            snapshot = Formatter.read_snapshot(rf)
            print(snapshot)
            Formatter.write_snapshot(snapshot, wf)
