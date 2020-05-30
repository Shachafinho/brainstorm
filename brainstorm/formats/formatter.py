import pathlib

from brainstorm.utils.drivers import DirectoryFocusedConfig
from brainstorm.utils.drivers import FocusedDriverManager


formatter_manager = FocusedDriverManager(DirectoryFocusedConfig(
    search_dir=pathlib.Path(__file__).parent.absolute(),
    module_name='formatter',
    class_name='Formatter',
))


class Formatter:
    """A manager object to choose and relay a specific formatter implementation.

    Formatters are uniquely identified by their subdirectory name.
    """

    def __init__(self, format_tag):
        """Construct a Formatter manager object.

        Args:
            format_tag (str): The tag (name) of the specific format.
        """
        self._formatter_driver = formatter_manager.find_driver(format_tag)

    def read_user_information(self, input_obj):
        """Read user information from *input_obj*.

        Args:
            input_obj (bytes or stream): Plain data or a buffer-like object
              supporting *read* operations.

        Return:
            :class:`~brainstorm.common.UserInformation`:
              The read user information.
        """
        return self._formatter_driver.read_user_information(input_obj)

    def read_snapshot(self, input_obj):
        """Read a snapshot from *input_obj*.

        Args:
            input_obj (bytes or stream): Plain data or a buffer-like object
              supporting *read* operations.

        Return:
            :class:`~brainstorm.common.Snapshot`:
              The read snapshot.
        """
        return self._formatter_driver.read_snapshot(input_obj)

    def write_user_information(self, user_information_obj, output_obj=None):
        """Write the specified user information to *output_obj*.

        Specifying a None *output_obj* simply returns the user information
        bytes.

        Args:
            user_information_obj (:class:`~brainstorm.common.UserInformation`):
              The user information object to write.
            output_obj (None or stream): None or a buffer-like object
              supporting *write* operations.

        Return:
            bytes: The written user information bytes representation.
        """
        return self._formatter_driver.write_user_information(
            user_information_obj, output_obj)

    def write_snapshot(self, snapshot_obj, output_obj=None):
        """Write the specified snapshot to *output_obj*.

        Specifying a None *output_obj* simply returns the snapshot bytes.

        Args:
            snapshot_obj (:class:`~brainstorm.common.Snapshot`):
              The snapshot object to write.
            output_obj (None or stream): None or a buffer-like object
              supporting *write* operations.

        Return:
            bytes: The written snapshot bytes representation.
        """
        return self._formatter_driver.write_snapshot(
            snapshot_obj, output_obj)
