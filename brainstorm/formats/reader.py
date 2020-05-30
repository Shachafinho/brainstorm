import contextlib

from .formatter import Formatter


class Reader:
    """A manager object to choose and relay a specific reader implementation.
    """

    def __init__(self, format_tag, stream):
        """Construct a Reader manager object.

        Args:
            format_tag (str): The tag (name) of the specific format.
            stream (stream): A buffer-like object supporting *read* operations.
        """
        self._reader_driver = Formatter(format_tag)
        self._stream = stream
        self._user_information = None
        self._user_information_end_location = None

    def _update_user_information(self):
        if self._user_information is None:
            self._user_information = \
                self._reader_driver.read_user_information(self._stream)
            self._user_information_end_location = self._stream.tell()

    @property
    def user_information(self):
        """Read user information from the stream.

        Return:
            :class:`~brainstorm.common.UserInformation`:
              The read user information.
        """
        self._update_user_information()
        return self._user_information

    @property
    def snapshots(self):
        """Read snapshots from the stream.

        Yield:
            :class:`~brainstorm.common.Snapshot`:
              The read snapshots.
        """
        self._update_user_information()
        self._stream.seek(self._user_information_end_location)
        with contextlib.suppress(EOFError):
            while True:
                yield self._reader_driver.read_snapshot(self._stream)
