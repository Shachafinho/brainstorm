from brainstorm.formats import Formatter
from brainstorm.sample import Reader
from brainstorm.utils import Connection


DEFAULT_FORMAT = 'protobuf'


def upload_sample(host, port, path):
    """Read the sample and send it to the server.

    Read the sample, specified by the given url: schema://path/to/sample.
    URL schema denotes the sample format.
    URL path/to/sample denotes the sample file location.

    Then, send the sample to the server using the specified host and port.

    Args:
        host (str): Server hostname to which the sample is uploaded.
        port (int): Server port to which the sample is uploaded.
        path (str): URL of the sample, where the schema determines the format.
    """
    format_tag = DEFAULT_FORMAT
    formatter = Formatter(format_tag)

    # Read the mind file to obtain user information and snapshots
    with Reader(path) as reader:
        user = reader.user_information
        for snapshot in reader.snapshots:
            with Connection.connect(host, port) as connection:
                print(f'Sending format message: {format_tag!r}...')
                connection.send_message(format_tag.encode())
                print('Done sending format message')

                print(f'Sending user message: {user}...')
                connection.send_message(formatter.write_user_information(user))
                print('Done sending user message')

                print(f'Sending snapshot message: {snapshot}...')
                connection.send_message(formatter.write_snapshot(snapshot))
                print('Done sending snapshot message')

                print()

    print('done')
