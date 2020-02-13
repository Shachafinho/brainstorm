import pathlib

from .binary import BinaryFileReader
from .protobuf import ProtobufReader


class Reader:
    def __init__(self, path):
        self.reader_driver = find_reader_driver(path)

    def __enter__(self):
        return self.reader_driver.__enter__()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return self.reader_driver.__exit__(exc_type, exc_value, exc_traceback)


def find_reader_driver(path):
    path = pathlib.Path(path)
    for ext, cls in reader_drivers.items():
        if ext == ''.join(path.suffixes):
            return cls(path)


reader_drivers = {
    '.mind': BinaryFileReader,
    '.mind.gz': ProtobufReader,
}


if __name__ == '__main__':
    path = '/home/user/Downloads/sample.mind'
    with Reader(path) as reader:
        print(reader.user_information)
        for snapshot in reader.snapshots:
            print(snapshot)
