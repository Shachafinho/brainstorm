import json
import pathlib

from brainstorm.formats import Formatter
from brainstorm.utils.paths import ROOT_DIR


DEFAULT_DATA_DIR = ROOT_DIR.parent / 'data'
DEFAULT_FORMATTER = Formatter('protobuf')


def _get_user_dir(user_information, data_dir=None):
    data_dir = pathlib.Path(str(data_dir)) if data_dir else DEFAULT_DATA_DIR
    return data_dir / str(user_information.user_id)


def _get_user_information_path(user_information, data_dir=None):
    return _get_user_dir(user_information, data_dir) / 'info'


def _get_snapshot_path(user_information, snapshot, data_dir=None):
    timestamp_str = snapshot.timestamp.format('YYYY-MM-DD_HH-mm-ss-SSSSSS')
    return _get_user_dir(user_information, data_dir) / timestamp_str


def _create_parent_dirs(file_path):
    file_path.parent.mkdir(mode=0o775, parents=True, exist_ok=True)


class Message:
    SNAPSHOT_FIELD = 'snapshot'
    USER_INFORMATION_FIELD = 'user_information'

    def __init__(self, user_information, snapshot):
        self.user_information = user_information
        self.snapshot = snapshot

    def serialize(self, data_dir=None, format_tag=None):
        formatter = Formatter(format_tag) if format_tag else DEFAULT_FORMATTER

        user_information_path = _get_user_information_path(
            self.user_information, data_dir=data_dir)
        if not user_information_path.exists():
            _create_parent_dirs(user_information_path)
            with open(user_information_path, 'w+b') as f:
                formatter.write_user_information(self.user_information, f)

        snapshot_path = _get_snapshot_path(
            self.user_information, self.snapshot, data_dir=data_dir)
        if not snapshot_path.exists():
            _create_parent_dirs(snapshot_path)
            with open(snapshot_path, 'w+b') as f:
                formatter.write_snapshot(self.snapshot, f)

        return json.dumps({
            self.USER_INFORMATION_FIELD: str(user_information_path),
            self.SNAPSHOT_FIELD: str(snapshot_path),
        }).encode()

    @classmethod
    def deserialize(cls, data, format_tag=None):
        formatter = Formatter(format_tag) if format_tag else DEFAULT_FORMATTER

        obj = json.loads(data.decode())
        with open(obj[cls.USER_INFORMATION_FIELD], 'rb') as f:
            user_information = formatter.read_user_information(f)
        with open(obj[cls.SNAPSHOT_FIELD], 'rb') as f:
            snapshot = formatter.read_snapshot(f)

        return cls(user_information, snapshot)
