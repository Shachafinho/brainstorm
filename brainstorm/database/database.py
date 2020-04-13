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
    def __init__(self, url, blob_store=None):
        url = furl(url)
        driver_cls = db_manager.find_driver(url.scheme)
        self._driver = driver_cls(url)
        self._blob_store = blob_store or BlobStore(DEFAULT_DATA_DIR)

    @property
    def blob_store(self):
        return self._blob_store

    def __enter__(self):
        self._driver.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return self._driver.__exit__(exc_type, exc_value, exc_traceback)
    
    def get_users(self):
        return self._driver.get_users()

    def get_user(self, user_id):
        return self._driver.get_user(user_id)

    def save_user(self, user_obj):
        return self._driver.save_user(user_obj)

    def get_snapshots(self, user_id):
        return self._driver.get_snapshots(user_id)

    def get_snapshot(self, user_id, snapshot_timestamp):
        return self._driver.get_snapshot(user_id, snapshot_timestamp)

    def save_snapshot(self, user_id, snapshot_obj):
        return self._driver.save_snapshot(user_id, snapshot_obj)

    def get_results(self, user_id, snapshot_timestamp):
        return self._driver.get_results(user_id, snapshot_timestamp)

    def get_result(self, user_id, snapshot_timestamp, result_name):
        return self._driver.get_result(
            user_id, snapshot_timestamp, result_name)

    def save_result(self, user_id, snapshot_timestamp, result_name,
                    result_obj):
        return self._driver.save_result(
            user_id, snapshot_timestamp, result_name, result_obj)
