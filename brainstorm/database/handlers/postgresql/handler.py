import contextlib
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


@contextlib.contextmanager
def _reraise_db_errors_context():
    try:
        yield
    except (psycopg2.Error) as e:
        raise DBError(f'DB operation failed: {e}') from e


def _reraise_db_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with _reraise_db_errors_context():
            return func(*args, **kwargs)
    return wrapper


class Handler:
    @_reraise_db_errors
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
        if self.connection is not None:
            self.connection.__exit__(exc_type, exc_value, exc_traceback)
            self.connection.close()

    @_reraise_db_errors
    def get_users(self):
        with self.connection:
            return user.get_users(self.connection)

    @_reraise_db_errors
    def get_user(self, user_id):
        with self.connection:
            return user.get_user(self.connection, user_id)

    @_reraise_db_errors
    def save_user(self, user_obj):
        with self.connection:
            return user.save_user(self.connection, user_obj)

    @_reraise_db_errors
    def get_snapshots(self, user_id):
        with self.connection:
            return snapshot.get_snapshots(self.connection, user_id)

    @_reraise_db_errors
    def get_snapshot(self, user_id, snapshot_timestamp):
        with self.connection:
            return snapshot.get_snapshot(
                self.connection, user_id, snapshot_timestamp)

    @_reraise_db_errors
    def save_snapshot(self, user_id, snapshot_obj):
        with self.connection:
            return snapshot.save_snapshot(
                self.connection, user_id, snapshot_obj)

    @_reraise_db_errors
    def get_results(self, user_id, snapshot_timestamp):
        with self.connection:
            return results.get_results(
                self.connection, user_id, snapshot_timestamp)

    @_reraise_db_errors
    def get_result(self, user_id, snapshot_timestamp, result_name):
        with self.connection:
            return results.get_result(
                self.connection, user_id, snapshot_timestamp, result_name)

    @_reraise_db_errors
    def save_result(self, user_id, snapshot_timestamp, result_name,
                    result_obj):
        with self.connection:
            return results.save_result(
                self.connection, user_id, snapshot_timestamp, result_name,
                result_obj)
