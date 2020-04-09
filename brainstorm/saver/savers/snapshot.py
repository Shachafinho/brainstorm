from brainstorm.database.objects import Snapshot
from brainstorm.message_queue import Topic


class SnapshotSaver:
    topic = 'snapshot'

    def __call__(self, database, data):
        context, mq_snapshot = Topic(self.topic).deserialize(data)
        print(f'Saving MQ snapshot data: {data}')
        context.save('snapshot.raw', data)

        database.save_snapshot(context.user_id, Snapshot(
            mq_snapshot.timestamp,
        ))
