"""
The parsers subpackage exposes the following API:

.. code-block:: python

    >>> from brainstorm.parsers import parse
    >>> data = ...
    >>> result = parse('pose', data)

Which accepts a parser name and some raw data, as consumed from the message
queue, and returns the result, as published to the message queue.

It also provides the following CLI:

.. code-block:: sh

    $ python -m brainstorm.parsers parse 'pose' 'snapshow.raw' > 'pose.result'

Which accepts a parser name and a path to some raw data, as consumed from the
message queue, and prints the result, as published to the message queue
(optionally redirecting it to a file). This way of invocation runs the parser
exactly once.

In addition, it supports running the parser as a service, which works with a
message queue indefinitely:

.. code-block:: sh

    $ python -m brainstorm.parsers run-parser 'pose' \
'rabbitmq://127.0.0.1:5672/'


Add a new parser
----------------
#. Create a python module under :file:`brainstorm/parsers/parsers/`.
#. Implement either of the following drivers:

    * Class (named ``XxxParser``), having a ``__call__`` method.
    * Function (named ``parse_xxx``).

   Both functions accept a :class:`~brainstorm.message_queue.Context`
   and an :mod:`MQ object <brainstorm.message_queue.objects>` to parse, and
   return an :mod:`MQ object <brainstorm.message_queue.objects>` as a result.

Example:
    .. literalinclude:: ../../brainstorm/parsers/parsers/echo.py
"""

from .bound_parser import BoundParser
from .bound_parser import parse
from .parser import Parser


__all__ = ['BoundParser', 'parse', 'Parser']
