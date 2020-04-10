import arrow

from brainstorm.database.objects import User


_GET_USERS = '''
    SELECT *
    FROM users;
'''

_GET_USER = '''
    SELECT *
    FROM users
    WHERE id = %s;
'''

_ADD_USER = '''
    INSERT INTO users(id, name, birthday, gender)
    VALUES(%s, %s, %s, %s);
'''


def user_information_from_row(row):
    user_id, name, birthday_str, gender = row
    return User(user_id, name, arrow.get(birthday_str), gender)


def get_users(connection):
    rows = []
    with connection.cursor() as cur:
        cur.execute(_GET_USERS)
        rows = cur.fetchall()
    return [user_information_from_row(row) for row in rows]


def get_user(connection, user_id):
    row = None
    with connection.cursor() as cur:
        cur.execute(_GET_USER, (user_id,))
        row = cur.fetchone()
    return user_information_from_row(row) if row is not None else None


def save_user(connection, user):
    args = (user.user_id, user.name, str(user.birthday), user.gender)
    with connection.cursor() as cur:
        cur.execute(_ADD_USER, args)
        connection.commit()
