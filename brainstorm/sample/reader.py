from brainstorm.formats.formatter_manager import formatter_manager
from brainstorm.formats.opener import get_opener


class Reader:
    def __init__(self, fmt, path):
        self._stream = None
        self._path = path
        self._opener = get_opener(path)
        self._reader_driver = formatter_manager.find_driver(fmt).reader

    def __enter__(self):
        self._stream = self._opener(self._path, 'rb').__enter__()
        return self._reader_driver(self._stream)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._stream.__exit__(exc_type, exc_value, exc_traceback)


if __name__ == '__main__':
    path = '/home/user/Downloads/sample.mind.gz'
    with Reader('protobuf', path) as reader:
        print(reader.user_information)
        for snapshot in reader.snapshots:
            print(snapshot)
