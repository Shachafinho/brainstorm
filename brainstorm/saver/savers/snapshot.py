from brainstorm.database.objects import Snapshot
from brainstorm.message_queue import Topic


def _mq_to_db(mq_snapshot):
    return Snapshot(mq_snapshot.timestamp)


class SnapshotSaver:
    topic = 'snapshot'

    def __call__(self, database, data):
        context, mq_snapshot = Topic(self.topic).deserialize(data)
        print(f'Saving MQ snapshot data: {data}')
        context.save('snapshot.raw', data)

        user_id = context.user_id

        # Ensure the snapshot doesn't already exist in the DB.
        if database.get_snapshot(user_id, mq_snapshot.timestamp):
            return

        # Save the snapshot to the DB.
        database.save_snapshot(user_id, _mq_to_db(mq_snapshot))
