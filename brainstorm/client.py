import socket

from datetime import datetime

from cli import CommandLineInterface
from connection import Connection
from thought import Thought


cli = CommandLineInterface()


@cli.command
def upload(address, user, thought):
    ip, port = address.split(':')
    user_id = int(user)

    upload_thought((ip, int(port)), user_id, thought)


def upload_thought(address, user, thought):
    # Send the thought to the server.
    with Connection.connect(address) as connection:
        connection.send(Thought(user, datetime.now(), thought).serialize())

    print('done')


if __name__ == '__main__':
    cli.main()
