import contextlib

import flask
import furl.furl as furl

from .errors import create_error_response
from .snapshots import get_snapshot_timestamp_by_id

from brainstorm.api.objects import BadRequestError
from brainstorm.api.objects import ColorImage
from brainstorm.api.objects import DepthImage
from brainstorm.api.objects import Feelings
from brainstorm.api.objects import NotFoundError
from brainstorm.api.objects import Pose
from brainstorm.api.objects import Rotation
from brainstorm.api.objects import Translation

from brainstorm.database.objects import ColorImage as DBColorImage
from brainstorm.database.objects import DepthImage as DBDepthImage
from brainstorm.database.objects import Feelings as DBFeelings
from brainstorm.database.objects import Pose as DBPose


_DATA_TOKEN_FIELD = 'data_token'
_DATA_PATH_COMPONENT = 'data'


def _db_color_image_to_color_image(db_color_image):
    return ColorImage(
        db_color_image.width,
        db_color_image.height,
        str(furl(flask.request.base_url) / _DATA_PATH_COMPONENT),
    )


def _db_depth_image_to_depth_image(db_depth_image):
    return DepthImage(
        db_depth_image.width,
        db_depth_image.height,
        str(furl(flask.request.base_url) / _DATA_PATH_COMPONENT),
    )


def _db_feelings_to_feelings(db_feelings):
    return Feelings(
        db_feelings.hunger,
        db_feelings.thirst,
        db_feelings.exhaustion,
        db_feelings.happiness,
    )


def _db_pose_to_pose(db_pose):
    return Pose(
        _db_translation_to_translation(db_pose.translation),
        _db_rotation_to_rotation(db_pose.rotation),
    )


def _db_rotation_to_rotation(db_rotation):
    return Rotation(
        db_rotation.x,
        db_rotation.y,
        db_rotation.z,
        db_rotation.w,
    )


def _db_translation_to_translation(db_translation):
    return Translation(
        db_translation.x,
        db_translation.y,
        db_translation.z,
    )


_MAPPING = {
    DBColorImage: _db_color_image_to_color_image,
    DBDepthImage: _db_depth_image_to_depth_image,
    DBFeelings: _db_feelings_to_feelings,
    DBPose: _db_pose_to_pose,
}


def _db_result_to_result(db_result):
    try:
        return _MAPPING[db_result.__class__](db_result)
    except KeyError:
        raise ValueError(f'Unknown result: {db_result!r}')


def get_result(database, user_id, snapshot_id, result_name):
    snapshot_timestamp = get_snapshot_timestamp_by_id(
        database, user_id, snapshot_id)

    try:
        db_result = database.get_result(
            user_id, snapshot_timestamp, result_name)
    except Exception:
        return create_error_response(
            BadRequestError(f'Result {result_name!r} is invalid'))

    if db_result is None:
        return create_error_response(
            NotFoundError(f'Result {result_name!r} was not found'))

    result = _db_result_to_result(db_result)
    serialized_result = result.serialize()
    return serialized_result


def get_result_data(database, user_id, snapshot_id, result_name):
    snapshot_timestamp = get_snapshot_timestamp_by_id(
        database, user_id, snapshot_id)

    db_result = database.get_result(user_id, snapshot_timestamp, result_name)
    data_token = getattr(db_result, _DATA_TOKEN_FIELD, None)
    if data_token is None:
        return create_error_response(
            BadRequestError(f'Result has no data field'))

    data = None
    with contextlib.suppress(Exception):
        data = database.blob_store.load(data_token)
    if data is None:
        return create_error_response(
            NotFoundError(f'Result data was not found'))

    return flask.Response(data, content_type='image/*')
