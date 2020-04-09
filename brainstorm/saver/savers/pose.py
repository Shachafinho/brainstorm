from brainstorm.database.objects import Pose
from brainstorm.database.objects import Rotation
from brainstorm.database.objects import Translation
from brainstorm.message_queue import Topic


class PoseSaver:
    topic = 'pose'

    def __call__(self, database, data):
        context, mq_pose = Topic(self.topic).deserialize(data)
        print(f'Saving MQ pose data: {data}')
        context.save('pose.raw', data)

        database.save_result(
            context.user_id, context.snapshot_timestamp, 'pose', Pose(
                Translation(
                    mq_pose.translation.x,
                    mq_pose.translation.y,
                    mq_pose.translation.z),
                Rotation(
                    mq_pose.rotation.x,
                    mq_pose.rotation.y,
                    mq_pose.rotation.z,
                    mq_pose.rotation.w),
            )
        )
