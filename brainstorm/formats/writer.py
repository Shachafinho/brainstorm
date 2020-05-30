from .formatter import Formatter


class Writer:
    """A manager object to choose and relay a specific writer implementation.
    """

    def __init__(self, format_tag, stream):
        """Construct a Writer manager object.

        Args:
            format_tag (str): The tag (name) of the specific format.
            stream (stream): A buffer-like object supporting *write*
              operations.
        """
        self._writer_driver = Formatter(format_tag)
        self._stream = stream

    @property
    def user_information(self):
        """Write the specified user information to the stream.

        Args:
            user_information (:class:`~brainstorm.common.UserInformation`):
              The user information object to write.
        """
        pass

    @user_information.setter
    def user_information(self, user_information):
        self._writer_driver.write_user_information(
            user_information, self._stream)

    @property
    def snapshot(self):
        """Write the specified snapshot to the stream.

        Args:
            snapshot_obj (:class:`~brainstorm.common.Snapshot`):
              The snapshot object to write.
        """
        pass

    @snapshot.setter
    def snapshot(self, snapshot):
        self._writer_driver.write_snapshot(snapshot, self._stream)

    @property
    def snapshots(self):
        """Write the specified snapshots to the stream.

        Args:
            snapshots (list(:class:`~brainstorm.common.Snapshot`)):
              A collection of snapshot objects to write.
        """
        pass

    @snapshots.setter
    def snapshots(self, snapshots):
        for snapshot in snapshots:
            self.snapshot = snapshot
