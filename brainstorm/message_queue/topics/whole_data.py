from brainstorm.message_queue.objects import WholeData


def serialize(context, whole_data):
    return whole_data.serialize(context)


def deserialize(context, serialized_whole_data):
    return WholeData.deserialize(context, serialized_whole_data)
