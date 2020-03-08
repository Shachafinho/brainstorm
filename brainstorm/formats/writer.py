import pathlib

from brainstorm.utils.drivers import FocusedConfig
from brainstorm.utils.drivers import FocusedDriverManager


writer_manager = FocusedDriverManager(FocusedConfig(
    search_dir=pathlib.Path(__file__).parent.absolute(),
    module_name='writer',
    class_name='Writer',
))


class Writer:
    def __init__(self, format_tag, stream):
        writer_driver_cls = writer_manager.find_driver(format_tag)
        self._writer_driver = writer_driver_cls(stream)

    @property
    def user_information(self):
        return self._writer_driver.user_information

    @user_information.setter
    def user_information(self, user_information):
        self._writer_driver.user_information = user_information

    @property
    def snapshot(self):
        return self._writer_driver.snapshot

    @snapshot.setter
    def snapshot(self, snapshot):
        self._writer_driver.snapshot = snapshot

    @property
    def snapshots(self):
        return self._writer_driver.snapshots

    @snapshots.setter
    def snapshots(self, snapshots):
        self._writer_driver.snapshots = snapshots

    def write_user_information(self, user_information_obj, output_obj=None):
        return self._writer_driver.write_user_information(
            user_information_obj, output_obj)

    def write_snapshot(self, snapshot_obj, output_obj=None):
        return self._writer_driver.write_snapshot(snapshot_obj, output_obj)
