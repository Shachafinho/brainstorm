import datetime as dt

from brainstorm.thought import Thought
from brainstorm.utils import Connection


def upload_thought(address, user, thought):
    # Send the thought to the server.
    with Connection.connect(*address) as connection:
        connection.send(Thought(user, dt.datetime.now(), thought).serialize())

    print('done')
