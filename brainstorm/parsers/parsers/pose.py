from brainstorm.message_queue.objects import Pose
from brainstorm.message_queue.objects import Rotation
from brainstorm.message_queue.objects import Translation


class PoseParser:
    tag = 'pose'
    bindings = ('snapshot', tag)

    def __call__(self, context, mq_snapshot):
        translation = Translation(
            mq_snapshot.pose.translation.x,
            mq_snapshot.pose.translation.y,
            mq_snapshot.pose.translation.z,
        )
        rotation = Rotation(
            mq_snapshot.pose.rotation.x,
            mq_snapshot.pose.rotation.y,
            mq_snapshot.pose.rotation.z,
            mq_snapshot.pose.rotation.w,
        )
        return context, Pose(translation, rotation)
