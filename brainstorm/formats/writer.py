from .formatter import Formatter


class Writer:
    def __init__(self, format_tag, stream):
        self._writer_driver = Formatter(format_tag)
        self._stream = stream

    @property
    def user_information(self):
        pass

    @user_information.setter
    def user_information(self, user_information):
        self._writer_driver.write_user_information(
            user_information, self._stream)

    @property
    def snapshot(self):
        pass

    @snapshot.setter
    def snapshot(self, snapshot):
        self._writer_driver.write_snapshot(snapshot, self._stream)

    @property
    def snapshots(self):
        pass

    @snapshots.setter
    def snapshots(self, snapshots):
        for snapshot in snapshots:
            self.snapshot = snapshot
