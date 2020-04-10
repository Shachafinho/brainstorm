from brainstorm.message_queue.objects import Feelings


def serialize(context, feelings):
    return feelings.serialize(context)


def deserialize(serialized_feelings):
    return Feelings.deserialize(serialized_feelings)
