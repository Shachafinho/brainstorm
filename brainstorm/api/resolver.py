import functools

import connexion


class DatabaseAwareResolver(connexion.Resolver):
    """A resolver object which injects a database object to its functions.
    """

    def __init__(self, database):
        """Construct a DatabaseAwareResolver object.

        Args:
            database (:class:`~brainstorm.database.Database`):
              The database object to inject to the resolved functions.
        """
        super(DatabaseAwareResolver, self).__init__()
        self._database = database

    def resolve_function_from_operation_id(self, operation_id):
        """Call super's implementation with the database as first parameter.
        """
        resolved_func = super(DatabaseAwareResolver, self)\
            .resolve_function_from_operation_id(operation_id)

        @functools.wraps(resolved_func)
        def wrapper(*args, **kwargs):
            return resolved_func(self._database, *args, **kwargs)
        return wrapper
