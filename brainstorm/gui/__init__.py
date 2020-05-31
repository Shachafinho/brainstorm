"""
The GUI exposes the following API:

.. code-block:: python

    >>> from brainstorm.gui import run_server
    >>> run_server(
    ...     host='127.0.0.1',
    ...     port=8080,
    ...     api_host='127.0.0.1'
    ...     api_port=5000
    ... )
    ... # listen on host:port and consume API from api_host:api_port

It also provides the following CLI:

.. code-block:: sh

    $ python -m brainstorm.gui run-server \\
        -h/--host '127.0.0.1' \\
        -p/--port 8080 \\
        -H/--api-host '127.0.0.1' \\
        -P/--api-port 5000
"""

from .server import run_server


__all__ = ['run_server']
