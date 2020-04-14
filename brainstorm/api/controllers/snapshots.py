from brainstorm.api.objects import Error
from brainstorm.api.objects import MinimalSnapshot
from brainstorm.api.objects import Snapshot


def _db_snapshot_to_minimal_snapshot(db_snapshot):
    return MinimalSnapshot(db_snapshot.timestamp)


def _create_snapshot(db_snapshot, results):
    minimal_snapshot = _db_snapshot_to_minimal_snapshot(db_snapshot)
    return Snapshot(minimal_snapshot.timestamp, results)


def get_snapshots(database, user_id):
    db_snapshots = database.get_snapshots(user_id)
    return [_db_snapshot_to_minimal_snapshot(db_snapshot).serialize()
            for db_snapshot in db_snapshots]


def get_snapshot(database, user_id, snapshot_timestamp):
    db_snapshot = database.get_snapshot(user_id, snapshot_timestamp)
    if db_snapshot is None:
        error = Error(404, f'Snapshot {snapshot_timestamp} was not found')
        return error.serialize(), 404

    results = database.get_results(user_id, snapshot_timestamp)
    return _create_snapshot(db_snapshot, results).serialize()
