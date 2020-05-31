"""
The server exposes the following API:

.. code-block:: python

    >>> from brainstorm.server import run_server
    >>> def print_message(message):
    ...     print(message)
    >>> run_server(
    ...     host='127.0.0.1',
    ...     port=8000,
    ...     publish=print_message
    ... )
    ... # listen on host:port and pass received messages to publish

It also provides the following CLI:

.. code-block:: sh

    $ python -m brainstorm.server run-server \\
        -h/--host '127.0.0.1' \\
        -p/--port 8000 \\
        'rabbitmq://127.0.0.1:5672/'

Note:
    The API lets callers pass any publishing function, while the CLI only lets
    them pass a URL to a message queue, to which the server then connects and
    publishes the data.
"""

from .server import run_server


__all__ = ['run_server']
