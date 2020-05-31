"""
The CLI consumes the API and reflects it:

* get-users

    Returns the list of all the supported users, including their IDs and names
    only.

    .. code-block:: sh

        $ python -m brainstorm.cli get-users \\
            -h/--host '127.0.0.1' \\
            -p/--port 5000

* get-user

    Returns the specified user's (``1``) details: ID, name, birthday and
    gender.

    .. code-block:: sh

        $ python -m brainstorm.cli get-user 1 \\
            -h/--host '127.0.0.1' \\
            -p/--port 5000

* get-snapshots

    Returns the list of the specified user's (``1``) snapshot IDs and
    datetimes only.

    .. code-block:: sh

        $ python -m brainstorm.cli get-snapshots 1 \\
            -h/--host '127.0.0.1' \\
            -p/--port 5000

* get-snapshot

    Returns the specified snapshot's (``2``) details: ID, datetime, and the
    available results' names only (e.g. *pose*).

    .. code-block:: sh

        $ python -m brainstorm.cli get-snapshot 1 2 \\
            -h/--host '127.0.0.1' \\
            -p/--port 5000

* get-result

    Returns the specified snapshot's result (``'pose'``). Any result having
    large binary data contains its metadata, with a dedicated URL referring to
    it.

    .. code-block:: sh

        $ python -m brainstorm.cli get-result 1 2 'pose' \\
            -h/--host '127.0.0.1' \\
            -p/--port 5000

    This command also accepts the ``-s``/``--save`` flag that, if specified,
    receives a path and saves the result's data to that path.

    .. code-block:: sh

        $ python -m brainstorm.cli get-result 1 2 'pose' \\
            -h/--host '127.0.0.1' \\
            -p/--port 5000 \\
            -s/--save 'path/to/result/file'
"""
