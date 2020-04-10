from brainstorm.message_queue.objects import Pose
from brainstorm.message_queue.objects import Rotation
from brainstorm.message_queue.objects import Translation


class PoseParser:
    tag = 'pose'
    bindings = ('snapshot', tag)

    def __call__(self, context, snapshot):
        translation = Translation(
            snapshot.pose.translation.x,
            snapshot.pose.translation.y,
            snapshot.pose.translation.z,
        )
        rotation = Rotation(
            snapshot.pose.rotation.x,
            snapshot.pose.rotation.y,
            snapshot.pose.rotation.z,
            snapshot.pose.rotation.w,
        )
        return Pose(translation, rotation)
