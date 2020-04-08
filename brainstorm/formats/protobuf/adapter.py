import arrow

from . import sample_pb2

from brainstorm.common import ColorImage
from brainstorm.common import DepthImage
from brainstorm.common import Feelings
from brainstorm.common import Pose
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
        birth_date=arrow.get(user_information_message.birthday),
        gender=_gender_to_str(user_information_message.gender),
    )


def translation_from_protobuf(translation_message):
    return Translation(
        x=translation_message.x,
        y=translation_message.y,
        z=translation_message.z,
    )


def rotation_from_protobuf(rotation_message):
    return Rotation(
        x=rotation_message.x,
        y=rotation_message.y,
        z=rotation_message.z,
        w=rotation_message.w,
    )


def pose_from_protobuf(pose_message):
    return Pose(
        translation=translation_from_protobuf(pose_message.translation),
        rotation=rotation_from_protobuf(pose_message.rotation),
    )


def color_image_from_protobuf(color_image_message):
    return ColorImage(
        width=color_image_message.width,
        height=color_image_message.height,
        data=color_image_message.data,
    )


def depth_image_from_protobuf(depth_image_message):
    return DepthImage(
        width=depth_image_message.width,
        height=depth_image_message.height,
        data=[num for num in depth_image_message.data],
    )


def feelings_from_protobuf(feelings_message):
    return Feelings(
        hunger=feelings_message.hunger,
        thirst=feelings_message.thirst,
        exhaustion=feelings_message.exhaustion,
        happiness=feelings_message.happiness,
    )


def snapshot_from_protobuf(snapshot_message):
    return Snapshot(
        timestamp=arrow.get(snapshot_message.datetime / 1000),
        pose=pose_from_protobuf(snapshot_message.pose),
        color_image=color_image_from_protobuf(snapshot_message.color_image),
        depth_image=depth_image_from_protobuf(snapshot_message.depth_image),
        feelings=feelings_from_protobuf(snapshot_message.feelings),
    )


def user_information_to_protobuf(user_information_obj):
    return sample_pb2.User(
        user_id=user_information_obj.user_id,
        username=user_information_obj.name,
        birthday=int(user_information_obj.birth_date.float_timestamp),
        gender=_str_to_gender(user_information_obj.gender),
    )


def translation_to_protobuf(translation_obj):
    return sample_pb2.Pose.Translation(
        x=translation_obj.x,
        y=translation_obj.y,
        z=translation_obj.z,
    )


def rotation_to_protobuf(rotation_obj):
    return sample_pb2.Pose.Rotation(
        x=rotation_obj.x,
        y=rotation_obj.y,
        z=rotation_obj.z,
        w=rotation_obj.w,
    )


def pose_to_protobuf(pose_obj):
    return sample_pb2.Pose(
        translation=translation_to_protobuf(pose_obj.translation),
        rotation=rotation_to_protobuf(pose_obj.rotation),
    )


def color_image_to_protobuf(color_image_obj):
    return sample_pb2.ColorImage(
        width=color_image_obj.width,
        height=color_image_obj.height,
        data=color_image_obj.data,
    )


def depth_image_to_protobuf(depth_image_obj):
    return sample_pb2.DepthImage(
        width=depth_image_obj.width,
        height=depth_image_obj.height,
        data=depth_image_obj.data,
    )


def feelings_to_protobuf(feelings_obj):
    return sample_pb2.Feelings(
        hunger=feelings_obj.hunger,
        thirst=feelings_obj.thirst,
        exhaustion=feelings_obj.exhaustion,
        happiness=feelings_obj.happiness,
    )


def snapshot_to_protobuf(snapshot_obj):
    return sample_pb2.Snapshot(
        datetime=int(snapshot_obj.timestamp.float_timestamp * 1000),
        pose=pose_to_protobuf(snapshot_obj.pose),
        color_image=color_image_to_protobuf(snapshot_obj.color_image),
        depth_image=depth_image_to_protobuf(snapshot_obj.depth_image),
        feelings=feelings_to_protobuf(snapshot_obj.feelings),
    )
