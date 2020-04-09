import arrow

from . import results
from brainstorm.database.objects import Snapshot


_GET_SNAPSHOTS = '''
    SELECT *
    FROM snapshots
    WHERE user_id = %s;
'''

_GET_SNAPSHOT = '''
    SELECT *
    FROM snapshots
    WHERE (user_id = %s AND timestamp = %s);
'''

_ADD_SNAPSHOT = '''
    INSERT INTO snapshots(user_id, timestamp)
    VALUES(%s, %s);
'''


def snapshot_from_row(row):
    user_id, timestamp_str = row
    return Snapshot(arrow.get(timestamp_str))


def get_snapshots(connection, user_id):
    rows = []
    with connection.cursor() as cur:
        cur.execute(_GET_SNAPSHOTS, (user_id,))
        rows = cur.fetchall()
    return map(snapshot_from_row, rows)


def get_snapshot(connection, user_id, snapshot_timestamp):
    row = None
    with connection.cursor() as cur:
        cur.execute(_GET_SNAPSHOT, (user_id, str(snapshot_timestamp)))
        row = cur.fetchone()
    return snapshot_from_row(row) if row is not None else None


def save_snapshot(connection, user_id, snapshot):
    snapshot_id = None
    with connection.cursor() as cur:
        cur.execute(_ADD_SNAPSHOT, (user_id, str(snapshot.timestamp)))
        connection.commit()
