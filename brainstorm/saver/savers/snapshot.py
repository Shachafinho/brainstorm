from brainstorm.database.objects import Snapshot
from brainstorm.message_queue import Topic


def _mq_to_db(mq_snapshot):
    return Snapshot(mq_snapshot.timestamp)


class SnapshotSaver:
    topic = 'snapshot'

    def __call__(self, database, data):
        context, mq_snapshot = Topic(self.topic).deserialize(data)
        print(f'Saving MQ snapshot data: {data}')
        context.save(data, subdir='snapshot', suffix='.raw')

        # Save the snapshot to the DB.
        database.save_snapshot(context.user_id, _mq_to_db(mq_snapshot))
