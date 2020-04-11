from brainstorm.message_queue.objects import Feelings


def serialize(context, feelings):
    return feelings.serialize(context)


def deserialize(context, serialized_feelings):
    return Feelings.deserialize(context, serialized_feelings)
