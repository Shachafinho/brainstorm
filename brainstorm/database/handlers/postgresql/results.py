import sys

import psycopg2

from brainstorm.utils.functions import get_module_functions


# TODO: Remove
'''
    SELECT
        (SELECT r.relname FROM pg_class r WHERE r.oid = c.conrelid) as table,
        (SELECT array_agg(attname) FROM pg_attribute
         WHERE attrelid = c.conrelid and ARRAY[attnum] <@ c.conkey) as col,
        (SELECT r.relname FROM pg_class r WHERE r.oid = c.confrelid) as ftable
    FROM pg_constraint c
    WHERE c.confrelid = (SELECT oid FROM pg_class WHERE relname = 'snapshots');
'''


_GET_REFERENCING_TABLES = '''
    SELECT
        (SELECT r.relname FROM pg_class r WHERE r.oid = c.conrelid) as table
    FROM pg_constraint c
    WHERE c.confrelid = (SELECT oid FROM pg_class WHERE relname = '{table}');
'''
_GET_SUPPORTED_RESULTS = _GET_REFERENCING_TABLES.format(table='snapshots')

_GET_RESULT = '''
    SELECT *
    FROM {table}
    WHERE (user_id = %s AND snapshot_timestamp = %s);
'''

_ADD_IMAGE = '''
    INSERT INTO {table}(user_id, snapshot_timestamp, width, height, data_token)
    VALUES(%s, %s, %s, %s, %s);
'''
_ADD_COLOR_IMAGE = _ADD_IMAGE.format(table='color_images')
_ADD_DEPTH_IMAGE = _ADD_IMAGE.format(table='depth_images')

_ADD_FEELINGS = '''
    INSERT INTO feelings(user_id, snapshot_timestamp,
                         hunger, thirst, exhaustion, happiness)
    VALUES(%s, %s, %s, %s, %s, %s);
'''

_ADD_POSE = '''
    INSERT INTO poses(user_id, snapshot_timestamp)
    VALUES(%s, %s);
'''

_ADD_ROTATION = '''
    INSERT INTO rotations(user_id, snapshot_timestamp, x, y, z, w)
    VALUES(%s, %s, %s, %s, %s, %s);
'''

_ADD_TRANSLATION = '''
    INSERT INTO translations(user_id, snapshot_timestamp, x, y, z)
    VALUES(%s, %s, %s, %s, %s);
'''


def _result_name_to_table(result_name):
    if result_name == 'feelings':
        return result_name
    return f'{result_name}s'


def _result_table_to_name(result_table):
    if result_table == 'feelings':
        return result_table
    return result_table[:-1]


def _get_supported_results(connection):
    rows = []
    with connection.cursor() as cur:
        cur.execute(_GET_SUPPORTED_RESULTS)
        rows = cur.fetchall()
    return [_result_table_to_name(row[0]) for row in rows]


def get_result(connection, user_id, snapshot_timestamp, result_name):
    row = None
    result_table = _result_name_to_table(result_name)
    args = (user_id, str(snapshot_timestamp))
    try:
        with connection.cursor() as cur:
            cur.execute(_GET_RESULT.format(table=result_table), args)
            row = cur.fetchone()
    except psycopg2.errors.UndefinedTable:
        # Ignore missing tables
        connection.rollback()

    return row if row is not None else None


def get_results(connection, user_id, snapshot_timestamp):
    supported_results = _get_supported_results(connection)
    return [result for result in supported_results if \
            get_result(connection, user_id, snapshot_timestamp, result)]


def _save_color_image(cursor, user_id, snapshot_timestamp, color_image):
    args = (user_id, str(snapshot_timestamp),
            color_image.width, color_image.height, color_image.data_token)
    cursor.execute(_ADD_COLOR_IMAGE, args)


def _save_depth_image(cursor, user_id, snapshot_timestamp, depth_image):
    args = (user_id, str(snapshot_timestamp),
            depth_image.width, depth_image.height, depth_image.data_token)
    cursor.execute(_ADD_DEPTH_IMAGE, args)


def _save_feelings(cursor, user_id, snapshot_timestamp, feelings):
    args = (user_id, str(snapshot_timestamp),
            feelings.hunger, feelings.thirst,
            feelings.exhaustion, feelings.happiness)
    cursor.execute(_ADD_FEELINGS, args)


def _save_pose(cursor, user_id, snapshot_timestamp, pose):
    cursor.execute(_ADD_POSE, (user_id, str(snapshot_timestamp)))
    _save_translation(cursor, user_id, snapshot_timestamp, pose.translation)
    _save_rotation(cursor, user_id, snapshot_timestamp, pose.rotation)


def _save_rotation(cursor, user_id, snapshot_timestamp, rotation):
    args = (user_id, str(snapshot_timestamp),
            rotation.x, rotation.y, rotation.z, rotation.w)
    cursor.execute(_ADD_ROTATION, args)


def _save_translation(cursor, user_id, snapshot_timestamp, translation):
    args = (user_id, str(snapshot_timestamp),
            translation.x, translation.y, translation.z)
    cursor.execute(_ADD_TRANSLATION, args)


_SAVERS = get_module_functions(sys.modules[__name__], r'_save_.*')


def _get_result_saver(result_name):
    try:
        return _SAVERS[f'_save_{result_name}']
    except KeyError:
        raise ValueError(f'Undefined result name: {result_name!r}')


def save_result(connection, user_id, snapshot_timestamp, result_name, result):
    with connection.cursor() as cur:
        result_saver = _get_result_saver(result_name)
        result_saver(cur, user_id, snapshot_timestamp, result)
        connection.commit()
