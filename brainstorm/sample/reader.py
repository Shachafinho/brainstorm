import furl.furl as furl

from brainstorm.formats.reader import Reader as FormatReader
from brainstorm.formats.opener import get_opener


class Reader:
    """An object responsible for reading user information and snapshots from
    sample files.
    """

    def __init__(self, url):
        """Construct a Reader object.

        Args:
            url (str): A URL representing the sample file to read.
              The scheme determines the format of the sample file (e.g.
              *protobuf*), whereas the path determines the local file path.
        """
        self._stream = None
        self._format_reader = None

        url = furl(url)
        self._path = str(url.path)
        self._opener = get_opener(self._path)
        self._sample_format = url.scheme

    def __enter__(self):
        self._stream = self._opener(self._path, 'rb').__enter__()
        self._format_reader = FormatReader(self._sample_format, self._stream)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._stream.__exit__(exc_type, exc_value, exc_traceback)

    @property
    def user_information(self):
        """Read user information from the file.

        Return:
            :class:`~brainstorm.common.UserInformation`:
              The read user information.
        """
        return self._format_reader.user_information

    @property
    def snapshots(self):
        """Read snapshots from the file.

        Yield:
            :class:`~brainstorm.common.Snapshot`:
              The read snapshots.
        """
        yield from self._format_reader.snapshots


if __name__ == '__main__':
    path = '/home/user/Downloads/sample.mind.gz'
    format_tag = 'protobuf'
    with Reader(furl(scheme=format_tag, path=path)) as reader:
        print(reader.user_information)
        for snapshot in reader.snapshots:
            print(snapshot)
