import pathlib

from brainstorm.utils.drivers import FocusedConfig
from brainstorm.utils.drivers import FocusedDriverManager


reader_manager = FocusedDriverManager(FocusedConfig(
    search_dir=pathlib.Path(__file__).parent.absolute(),
    module_name='reader',
    class_name='Reader',
))


class Reader:
    def __init__(self, format_tag, stream):
        reader_driver_cls = reader_manager.find_driver(format_tag)
        self._reader_driver = reader_driver_cls(stream)

    @property
    def user_information(self):
        return self._reader_driver.user_information

    @property
    def snapshots(self):
        yield from self._reader_driver.snapshots

    def read_user_information(self, input_obj):
        return self._reader_driver.read_user_information(input_obj)

    def read_snapshot(self, input_obj):
        return self._reader_driver.read_snapshot(input_obj)
