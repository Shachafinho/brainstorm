from brainstorm.formats import Formatter
from brainstorm.sample import Reader
from brainstorm.utils import Connection


DEFAULT_FORMAT = 'protobuf'


def upload_sample(host, port, path):
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
                print(f'Done sending snapshot message')

                print()

    print('done')
