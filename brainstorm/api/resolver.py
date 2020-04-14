import functools

import connexion


class DatabaseAwareResolver(connexion.Resolver):
    def __init__(self, database):
        super(DatabaseAwareResolver, self).__init__()
        self._database = database

    def resolve_function_from_operation_id(self, operation_id):
        resolved_func = super(DatabaseAwareResolver, self)\
            .resolve_function_from_operation_id(operation_id)

        @functools.wraps(resolved_func)
        def wrapper(*args, **kwargs):
            return resolved_func(self._database, *args, **kwargs)
        return wrapper
