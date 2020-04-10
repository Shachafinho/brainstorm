from brainstorm.message_queue.objects import Snapshot


def serialize(context, snapshot):
    return snapshot.serialize(context)


def deserialize(serialized_snapshot):
    return Snapshot.deserialize(serialized_snapshot)
