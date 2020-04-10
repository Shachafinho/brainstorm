class SnapshotParser:
    tag = 'snapshot'

    def __call__(self, context, mq_whole_data):
        context.user_id = mq_whole_data.user_information.user_id
        context.snapshot_timestamp = mq_whole_data.snapshot.timestamp
        return context, mq_whole_data.snapshot
