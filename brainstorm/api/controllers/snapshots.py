import contextlib

from .errors import create_error_response
from brainstorm.api.objects import MinimalSnapshot
from brainstorm.api.objects import NotFoundError
from brainstorm.api.objects import Snapshot


def _create_minimal_snapshot(snapshot_id, db_snapshot):
    return MinimalSnapshot(snapshot_id, db_snapshot.timestamp)


def _create_snapshot(snapshot_id, db_snapshot, results):
    minimal_snapshot = _create_minimal_snapshot(snapshot_id, db_snapshot)
    return Snapshot(minimal_snapshot.snapshot_id, minimal_snapshot.timestamp,
                    results)


def get_snapshots(database, user_id):
    db_snapshots = database.get_snapshots(user_id)
    return [_create_minimal_snapshot(i, db_snapshot).serialize()
            for i, db_snapshot in enumerate(db_snapshots, start=1)]


def get_snapshot_timestamp_by_id(database, user_id, snapshot_id):
    timestamp = None
    with contextlib.suppress(Exception):
        timestamp = database.get_snapshots(user_id)[snapshot_id - 1].timestamp
    return timestamp


def get_snapshot(database, user_id, snapshot_id):
    snapshot_timestamp = get_snapshot_timestamp_by_id(
        database, user_id, snapshot_id)
    if snapshot_timestamp is None:
        return create_error_response(
            NotFoundError(f'Snapshot ID {snapshot_id!r} was not found'))

    db_snapshot = database.get_snapshot(user_id, snapshot_timestamp)
    results = database.get_results(user_id, snapshot_timestamp)
    return _create_snapshot(snapshot_id, db_snapshot, results).serialize()
