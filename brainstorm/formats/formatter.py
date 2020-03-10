import pathlib

from brainstorm.utils.drivers import FocusedConfig
from brainstorm.utils.drivers import FocusedDriverManager


formatter_manager = FocusedDriverManager(FocusedConfig(
    search_dir=pathlib.Path(__file__).parent.absolute(),
    module_name='formatter',
    class_name='Formatter',
))


class Formatter:
    def __init__(self, format_tag):
        self._formatter_driver = formatter_manager.find_driver(format_tag)

    def read_user_information(self, input_obj):
        return self._formatter_driver.read_user_information(input_obj)

    def read_snapshot(self, input_obj):
        return self._formatter_driver.read_snapshot(input_obj)

    def write_user_information(self, user_information_obj, output_obj=None):
        return self._formatter_driver.write_user_information(
            user_information_obj, output_obj)

    def write_snapshot(self, snapshot_obj, output_obj=None):
        return self._formatter_driver.write_snapshot(
            snapshot_obj, output_obj)
