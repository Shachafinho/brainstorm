from brainstorm.protocol import Hello
from brainstorm.protocol import Config
from brainstorm.protocol import Snapshot
from brainstorm.sample import Reader
from brainstorm.utils import Connection


def build_protocol_snapshot(reader_snapshot, supported_fields):
    components = {field: getattr(reader_snapshot, field)
                  if field in supported_fields else None
                  for field in reader_snapshot.__slots__}
    components.update(timestamp=reader_snapshot.timestamp)

    return Snapshot(**components)


def share_mind(address, mind_file):
    # Read the mind file to obtain user information and snapshots
    with Reader(mind_file) as reader:
        user = reader.user_information
        hello = Hello(user.user_id, user.name, user.birth_date, user.gender)

        for reader_snapshot in reader.snapshots:
            with Connection.connect(*address) as connection:
                print(f'Sending hello message: {hello}...')
                connection.send_message(hello.serialize())
                print('Done sending hello message')

                print('Waiting for config message...')
                config = Config.deserialize(connection.receive_message())
                print(f'Got config message: {config}')

                snapshot = build_protocol_snapshot(
                    reader_snapshot, config.fields)
                print(f'Sending snapshot message: {snapshot}...')
                connection.send_message(snapshot.serialize())
                print(f'Done sending snapshot message')

                print()

    print('done')
