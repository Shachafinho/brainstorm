import pathlib

import furl.furl as furl

from brainstorm.utils.blob_store import BlobStore
from brainstorm.utils.drivers import DirectoryFocusedConfig
from brainstorm.utils.drivers import FocusedDriverManager
from brainstorm.utils.paths import ROOT_DIR


db_manager = FocusedDriverManager(DirectoryFocusedConfig(
    search_dir=pathlib.Path(__file__).parent.absolute() / 'handlers',
    module_name='handler',
    class_name='Handler',
))


DEFAULT_DATA_DIR = ROOT_DIR.parent / 'db_data'


class Database:
    """A manager object to choose and relay a specific DB implementation.
    """

    def __init__(self, url, blob_store=None):
        """Construct the Database manager object.

        Args:
            url (str): A URL representing the specific database to use.
              The scheme determines the type of the database (e.g.
              *postgresql*), whereas the host and port determine the address of
              the database.
        """
        url = furl(url)
        driver_cls = db_manager.find_driver(url.scheme)
        self._driver = driver_cls(url)
        self._blob_store = blob_store or BlobStore(DEFAULT_DATA_DIR)

    @property
    def blob_store(self):
        """A BlobStore object to handle large data.

        Return:
            :class:`~brainstorm.utils.blob_store.BlobStore`:
              A BlobStore object to handle large data.
        """
        return self._blob_store

    def __enter__(self):
        self._driver.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return self._driver.__exit__(exc_type, exc_value, exc_traceback)

    def get_users(self):
        """Return a list of all supported users.

        Return:
            list(:class:`~brainstorm.database.objects.User`):
              A list of all supported users.
        """
        return self._driver.get_users()

    def get_user(self, user_id):
        """Return the specified user's details.

        Args:
            user_id (int): ID of a specific user.

        Return:
            :class:`~brainstorm.database.objects.User`:
              Specified user's details.
        """
        return self._driver.get_user(user_id)

    def save_user(self, user_obj):
        """Store the user's details in the database.

        Args:
            user_obj (:class:`~brainstorm.database.objects.User`):
              User's details to store in the database.
        """
        self._driver.save_user(user_obj)

    def get_snapshots(self, user_id):
        """Return a list of the specified user's snapshots.

        Args:
            user_id (int): ID of a specific user.

        Return:
            list(:class:`~brainstorm.database.objects.Snapshot`):
              Specified user's snapshots.
        """
        return self._driver.get_snapshots(user_id)

    def get_snapshot(self, user_id, snapshot_timestamp):
        """Return the specified snapshot's details.

        Args:
            user_id (int): ID of the snapshot owner.
            snapshot_timestamp (:class:`arrow.Arrow`):
              Timestamp of the snapshot.

        Return:
            :class:`~brainstorm.database.objects.Snapshot`:
              Specified snapshot's details.
        """
        return self._driver.get_snapshot(user_id, snapshot_timestamp)

    def save_snapshot(self, user_id, snapshot_obj):
        """Store the snapshot's details in the database.

        Args:
            user_id (int): ID of the snapshot owner.
            snapshot_obj (:class:`~brainstorm.database.objects.Snapshot`):
              Snapshot's details to store in the database.
        """
        self._driver.save_snapshot(user_id, snapshot_obj)

    def get_results(self, user_id, snapshot_timestamp):
        """Return a list of the the specified snapshot's results names.

        Args:
            user_id (int): ID of the snapshot owner.
            snapshot_timestamp (:class:`arrow.Arrow`):
              Timestamp of the snapshot.

        Return:
            list(str): Specified snapshot's results names.
        """
        return self._driver.get_results(user_id, snapshot_timestamp)

    def get_result(self, user_id, snapshot_timestamp, result_name):
        """Return the specified result's details.

        Args:
            user_id (int): ID of the snapshot owner.
            snapshot_timestamp (:class:`arrow.Arrow`):
              Timestamp of the snapshot.
            result_name (str): Name of the result.

        Return:
            object: Specified result's details.
        """
        return self._driver.get_result(
            user_id, snapshot_timestamp, result_name)

    def save_result(self, user_id, snapshot_timestamp, result_name,
                    result_obj):
        """Store the result's details in the database.

        Args:
            user_id (int): ID of the snapshot owner.
            snapshot_timestamp (:class:`arrow.Arrow`):
              Timestamp of the snapshot.
            result_name (str): Name of the result.
            result_obj (object): Result's details to store in the database.
        """
        self._driver.save_result(
            user_id, snapshot_timestamp, result_name, result_obj)
