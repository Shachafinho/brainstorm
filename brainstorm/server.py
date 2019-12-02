import threading

from datetime import datetime
from pathlib import Path

from cli import CommandLineInterface
from listener import Listener
from thought import Thought


cli = CommandLineInterface()


class Handler(threading.Thread):
    def __init__(self, connection, data_dir, lock):
        super().__init__()
        self.conn = connection
        self.data_dir = data_dir
        self.lock = lock

    def run(self):
        # Obtain the thought header (as it is of fixed size),
        # and extract its components.
        header = self.conn.receive(Thought.get_header_size_in_bytes())
        user_id, timestamp, thought_size = \
            Thought.deserialize_header(header)

        # Obtain the thought data (using header) and deserialize the thought.
        thought_data = self.conn.receive(thought_size)
        thought = Thought.deserialize_data(thought_data)

        # Construct the complete thought.
        thought = Thought(user_id, timestamp, thought)

        # Write the thought to the disk.
        self.write_to_file(thought)

        # Print the thought
        print(thought)

    def get_file_path(self, user_id, timestamp):
        # Get the datetime string representation.
        datetime_str = timestamp.strftime('%Y-%m-%d_%H-%M-%S')

        # Return the full path.
        return Path(self.data_dir, str(user_id), datetime_str + '.txt')

    def write_to_file(self, thought):
        file_path = self.get_file_path(thought.user_id, thought.timestamp)
        text_to_write = thought.thought

        # Create directories along the path (as needed).
        file_path.parent.mkdir(mode=0o775, parents=True, exist_ok=True)

        with self.lock:
            # Separate thought messages with a line-break.
            if file_path.exists() and file_path.stat().st_size > 0:
                text_to_write = '\n' + text_to_write

            # Only access the file once the lock has been acquired.
            with open(file_path, 'a') as f:
                f.write(text_to_write)


@cli.command
def run(address, data):
    if ':' in address:
        ip, port = address.split(':')
    else:
        # Assume the supplied address consists of port only.
        ip, port = None, int(address)

    run_server((ip, port), data)


def run_server(address, data_dir):
    ip, port = address
    listener = Listener(port, ip) if ip else Listener(port)

    lock = threading.RLock()
    with listener:
        while True:
            connection = listener.accept()
            handler = Handler(connection, data_dir, lock)
            handler.start()


if __name__ == '__main__':
    cli.main()
