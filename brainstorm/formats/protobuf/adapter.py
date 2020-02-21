from arrow import Arrow

from . import sample_pb2

from brainstorm.common import ColorImage
from brainstorm.common import DepthImage
from brainstorm.common import Feelings
from brainstorm.common import Rotation
from brainstorm.common import Snapshot
from brainstorm.common import Translation
from brainstorm.common import UserInformation


_GENDER_TO_STR = {
    sample_pb2.User.Gender.MALE: 'm',
    sample_pb2.User.Gender.FEMALE: 'f',
    sample_pb2.User.Gender.OTHER: 'o',
}
_STR_TO_GENDER = {v: k for k, v in _GENDER_TO_STR.items()}


def _gender_to_str(gender):
    return _GENDER_TO_STR[gender]


def _str_to_gender(gender_str):
    return _STR_TO_GENDER[gender_str]


def user_information_from_protobuf(user_information_message):
    return UserInformation(
        user_id=user_information_message.user_id,
        name=user_information_message.username,
        birth_date=Arrow.utcfromtimestamp(user_information_message.birthday),
        gender=_gender_to_str(user_information_message.gender))


def snapshot_from_protobuf(snapshot_message):
    return Snapshot(
        timestamp=Arrow.utcfromtimestamp(snapshot_message.datetime / 1000),
        translation=Translation(
            x=snapshot_message.pose.translation.x,
            y=snapshot_message.pose.translation.y,
            z=snapshot_message.pose.translation.z,
        ),
        rotation=Rotation(
            x=snapshot_message.pose.rotation.x,
            y=snapshot_message.pose.rotation.y,
            z=snapshot_message.pose.rotation.z,
            w=snapshot_message.pose.rotation.w
        ),
        color_image=ColorImage(
            width=snapshot_message.color_image.width,
            height=snapshot_message.color_image.height,
            data=snapshot_message.color_image.data
        ),
        depth_image=DepthImage(
            width=snapshot_message.depth_image.width,
            height=snapshot_message.depth_image.height,
            data=snapshot_message.depth_image.data
        ),
        feelings=Feelings(
            hunger=snapshot_message.feelings.hunger,
            thirst=snapshot_message.feelings.thirst,
            exhaustion=snapshot_message.feelings.exhaustion,
            happiness=snapshot_message.feelings.happiness
        )
    )


def user_information_to_protobuf(user_information_obj):
    return sample_pb2.User(
        user_id=user_information_obj.user_id,
        username=user_information_obj.name,
        birthday=int(user_information_obj.birth_date.float_timestamp),
        gender=_str_to_gender(user_information_obj.gender))


def snapshot_to_protobuf(snapshot_obj):
    return sample_pb2.Snapshot(
        datetime=int(snapshot_obj.timestamp.float_timestamp * 1000),
        pose=sample_pb2.Pose(
            translation=sample_pb2.Pose.Translation(
                x=snapshot_obj.translation.x,
                y=snapshot_obj.translation.y,
                z=snapshot_obj.translation.z
            ),
            rotation=sample_pb2.Pose.Rotation(
                x=snapshot_obj.rotation.x,
                y=snapshot_obj.rotation.y,
                z=snapshot_obj.rotation.z,
                w=snapshot_obj.rotation.w
            )
        ),
        color_image=sample_pb2.ColorImage(
            width=snapshot_obj.color_image.width,
            height=snapshot_obj.color_image.height,
            data=snapshot_obj.color_image.data
        ),
        depth_image=sample_pb2.DepthImage(
            width=snapshot_obj.depth_image.width,
            height=snapshot_obj.depth_image.height,
            data=snapshot_obj.depth_image.data
        ),
        feelings=sample_pb2.Feelings(
            hunger=snapshot_obj.feelings.hunger,
            thirst=snapshot_obj.feelings.thirst,
            exhaustion=snapshot_obj.feelings.exhaustion,
            happiness=snapshot_obj.feelings.happiness
        )
    )
