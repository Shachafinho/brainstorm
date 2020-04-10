from brainstorm.message_queue.objects import Pose


def serialize(context, pose):
    return pose.serialize(context)


def deserialize(serialized_pose):
    return Pose.deserialize(serialized_pose)
