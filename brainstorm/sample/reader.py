from furl import furl

from brainstorm.formats.formatter_manager import reader_manager
from brainstorm.formats.opener import get_opener


class Reader:
    def __init__(self, url):
        self._stream = None

        url = furl(url)
        self._path = str(url.path)
        self._opener = get_opener(self._path)
        self._reader_driver = reader_manager.find_driver(url.scheme)

    def __enter__(self):
        self._stream = self._opener(self._path, 'rb').__enter__()
        return self._reader_driver(self._stream)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._stream.__exit__(exc_type, exc_value, exc_traceback)


if __name__ == '__main__':
    path = '/home/user/Downloads/sample.mind.gz'
    format_tag = 'uknown'
    with Reader(furl(scheme=format_tag, path=path)) as reader:
        print(reader.user_information)
        for snapshot in reader.snapshots:
            print(snapshot)
