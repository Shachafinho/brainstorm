from furl import furl

from brainstorm.formats.formatter_manager import reader_manager
from brainstorm.formats.opener import get_opener


class Reader:
    def __init__(self, url):
        self._stream = None
        self._reader_driver = None

        url = furl(url)
        self._path = str(url.path)
        self._opener = get_opener(self._path)
        self._reader_driver_cls = reader_manager.find_driver(url.scheme)

    def __enter__(self):
        self._stream = self._opener(self._path, 'rb').__enter__()
        self._reader_driver = self._reader_driver_cls(self._stream)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._stream.__exit__(exc_type, exc_value, exc_traceback)

    @property
    def user_information(self):
        return self._reader_driver.user_information

    @property
    def snapshots(self):
        yield from self._reader_driver.snapshots


if __name__ == '__main__':
    path = '/home/user/Downloads/sample.mind.gz'
    format_tag = 'protobuf'
    with Reader(furl(scheme=format_tag, path=path)) as reader:
        print(reader.user_information)
        for snapshot in reader.snapshots:
            print(snapshot)
