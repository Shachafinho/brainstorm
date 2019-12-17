Brainstorm API Reference
========================

This is Brainstorm's API reference.

Thought
-------

.. class:: brainstorm.Thought

    Represents a user's message at some given time.

    .. method:: init(user_id, timestamp, thought)

        :param int user_id: Thought owner's ID
        :param timestamp: The moment at which the thought was created
        :type timestamp: datetime.datetime
        :param str thought: The thought's message


    .. method:: serialize()

        Return the byte representation of the ``Thought`` object.

    .. classmethod:: deserialize(data)

        :param bytes data: The data from which a thought is created
        :raises ValueError: If thought header is of the wrong size

        Create a ``Thought`` object from the given ``data``.

run_server
----------

.. function:: run_server(address, data_dir)

    :param address: The address to which the server will bind
    :type address: tuple(str, int)
    :param str data_dir: Path to directory containing stored thoughts

    Run the central server, which accepts user's thoughts and stores them in the given ``data_dir``.


run_webserver
-------------

.. function:: run_webserver(address, data_dir)

    :param address: The address to which the server will bind
    :type address: tuple(str, int)
    :param str data_dir: Path to directory containing stored thoughts

    Run the web server, which shows users and their corresponding thoughts.


upload_thought
--------------

.. function:: upload_thought(address, user, thought)

    :param address: The server address to which the thought is uploaded
    :type address: tuple(str, int)
    :param int user: The user who owns the thought
    :param str thought: The thought message to be uploaded

    Upload ``thought`` by ``user`` to the server at ``address``.
