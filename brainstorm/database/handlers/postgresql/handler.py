import functools

import furl.furl as furl
import psycopg2

from . import results
from . import snapshot
from . import user
from brainstorm.database import DBError


POSTGRES_DB = 'brainstorm'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'password'


def safe_transaction(method):
    @functools.wraps(method)
    def _method(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except (psycopg2.Error, Exception) as e:
            if self.connection is not None:
                self.connection.rollback()
            raise DBError('DB operation failed') from e
    return _method


class Handler:
    def __init__(self, url):
        self._connection = None

        url = furl(url)
        username = url.username or POSTGRES_USER
        password = url.password or POSTGRES_PASSWORD

        # Connect to the PostgreSQL database server
        self._connection = psycopg2.connect(
            database=POSTGRES_DB, host=url.host, port=url.port,
            user=username, password=password)

    @property
    def connection(self):
        return self._connection

    def __enter__(self):
        self.connection.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.__exit__(exc_type, exc_value, exc_traceback)
        if self.connection is not None:
            self.connection.close()

    @safe_transaction
    def get_users(self):
        return user.get_users(self.connection)

    @safe_transaction
    def get_user(self, user_id):
        return user.get_user(self.connection, user_id)

    @safe_transaction
    def save_user(self, user_obj):
        return user.save_user(self.connection, user_obj)

    @safe_transaction
    def get_snapshots(self, user_id):
        return snapshot.get_snapshots(self.connection, user_id)

    @safe_transaction
    def get_snapshot(self, user_id, snapshot_timestamp):
        return snapshot.get_snapshot(
            self.connection, user_id, snapshot_timestamp)

    @safe_transaction
    def save_snapshot(self, user_id, snapshot_obj):
        return snapshot.save_snapshot(self.connection, user_id, snapshot_obj)

    @safe_transaction
    def get_results(self, user_id, snapshot_timestamp):
        return results.get_results(
            self.connection, user_id, snapshot_timestamp)

    @safe_transaction
    def get_result(self, user_id, snapshot_timestamp, result_name):
        return results.get_result(
            self.connection, user_id, snapshot_timestamp, result_name)

    @safe_transaction
    def save_result(self, user_id, snapshot_timestamp, result_name,
                    result_obj):
        return results.save_result(
            self.connection, user_id, snapshot_timestamp, result_name,
            result_obj)
