import arrow

import sample_pb2

from ...common import ColorImage
from ...common import DepthImage
from ...common import Feelings
from ...common import Rotation
from ...common import Snapshot
from ...common import Translation
from ...common import UserInformation


def user_information_from_protobuf(user_information_message):
    return UserInformation(
        user_id=user_information_message.user_id,
        name=user_information_message.username,
        birth_date=user_information_message.birthday,
        gender=user_information_message.gender)


def snapshot_from_protobuf(snapshot_message):
    return Snapshot(
        timestamp=arrow.Arrow.fromtimestamp(snapshot_message.datetime),
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
        birthday=user_information_obj.birth_date,
        gender=user_information_obj.gender)


def snapshot_to_protobuf(snapshot_obj):
    return sample_pb2.Snapshot(
        datetime=snapshot_obj.timestamp,
        pose=sample_pb2.Snapshot.Pose(
            translation=sample_pb2.Snapshot.Translation(
                x=snapshot_obj.translation.x,
                y=snapshot_obj.translation.y,
                z=snapshot_obj.translation.z
            ),
            rotation=sample_pb2.Snapshot.Rotation(
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
            thirst=snapshot_obj.feelings.thrist,
            exhaustion=snapshot_obj.feelings.exhaustion,
            happiness=snapshot_obj.feelings.happiness
        )
    )


# CONVERTERS_FROM_PROTOBUF = {
#     sample_pb2.User: user_information_from_protobuf,
#     sample_pb2.Snapshot: snapshot_from_protobuf,
# }

# CONVERTERS_TO_PROTOBUF = {
#     UserInformation: user_information_to_protobuf,
#     Snapshot: snapshot_to_protobuf,
# }


# def from_protobuf(message):
#     converter = CONVERTERS_FROM_PROTOBUF.get(message.__class__)
#     if converter:
#         return converter(message)
#     raise ValueError(f'{message} cannot be converted. '
#                      f'{message.__class__} is not supported')


# def to_protobuf(obj):
#     converter = CONVERTERS_TO_PROTOBUF.get(obj.__class__)
#     if converter:
#         return converter(obj)
#     raise ValueError(f'{obj} cannot be converted. '
#                      f'{obj.__class__} is not supported')
