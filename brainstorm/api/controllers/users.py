from .errors import create_error_response
from brainstorm.api.objects import MinimalUser
from brainstorm.api.objects import NotFoundError
from brainstorm.api.objects import User


def _db_user_to_minimal_user(db_user):
    return MinimalUser(db_user.user_id, db_user.name)


def _db_user_to_user(db_user):
    minimal_user = _db_user_to_minimal_user(db_user)
    return User(minimal_user.user_id, minimal_user.name,
                db_user.birthday, db_user.gender)


def get_users(database):
    db_users = database.get_users()
    return [_db_user_to_minimal_user(db_user).serialize()
            for db_user in db_users]


def get_user(database, user_id):
    db_user = database.get_user(user_id)
    if db_user is None:
        return create_error_response(
            NotFoundError(f'User ID {user_id!r} was not found'))

    return _db_user_to_user(db_user).serialize()
