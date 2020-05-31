"""
The saver exposes the following API:

.. code-block:: python

    >>> from brainstorm.saver import Saver
    >>> saver = Saver(database_url)
    >>> data = ...
    >>> saver.save('pose', data)

Which connects to a database, accepts a topic name and some data, as consumed
from the message queue, and saves it to the database.

It also provides the following CLI:

.. code-block:: sh

    $ python -m brainstorm.saver save \\
        -d/--database 'postgresql://127.0.0.1:5432/' \\
        'pose' \\
        'pose.result'

Which accepts a topic name and a path to some raw data, as consumed from the
message queue, and saves it to a database. This way of invocation runs the
saver exactly once

In addition, it supports running the saver as a service, which works with a
message queue indefinitely; it is then the saver's responsibility to subscribe
to all the relevant topics it is capable of consuming and saving to the
database.

.. code-block:: sh

    $ python -m brainstorm.saver run-saver \\
        'postgresql://127.0.0.1:5432/' \\
        'rabbitmq://127.0.0.1:5672/'


Add a new saver
----------------
#. Create a python module under :file:`brainstorm/saver/savers/`.
#. Implement either of the following drivers:

    * Class (named ``XxxSaver``), having a ``__call__`` method.
    * Function (named ``save_xxx``).

   Both functions accept a :class:`~brainstorm.database.Database` and a
   serialized data object (`bytes`) to deserialize and save to the database.
"""

from .saver import Saver


__all__ = ['Saver']
