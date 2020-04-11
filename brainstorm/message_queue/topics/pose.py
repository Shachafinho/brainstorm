from brainstorm.message_queue.objects import Pose


def serialize(context, pose):
    return pose.serialize(context)


def deserialize(context, serialized_pose):
    return Pose.deserialize(context, serialized_pose)
