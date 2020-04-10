import pathlib

import arrow

from brainstorm.utils.paths import ROOT_DIR


DEFAULT_DATA_DIR = ROOT_DIR.parent / 'mq_data'
TIMESTAMP_FORMAT = 'YYYY-MM-DD_HH-mm-ss-SSSSSS'


class Context:
    def __init__(self, user_id=None, snapshot_timestamp=None, data_dir=None):
        self.user_id = user_id
        self.snapshot_timestamp = snapshot_timestamp
        self.data_dir = pathlib.Path(str(data_dir)) if data_dir is not None \
            else DEFAULT_DATA_DIR

    def path(self, filename, *, create_dirs=True):
        user_id_str = str(self.user_id) if self.user_id is not None else ''
        timestamp_str = self.snapshot_timestamp.format(TIMESTAMP_FORMAT) \
            if self.snapshot_timestamp is not None else ''
        file_path = self.data_dir / user_id_str / timestamp_str / filename

        # Create directories along the path (as needed).
        if create_dirs:
            file_path.parent.mkdir(mode=0o775, parents=True, exist_ok=True)
        return file_path

    def save(self, filename, data):
        self.path(filename).write_bytes(data)

    def serialize(self):
        context_dict =  {
            'data_dir': str(self.data_dir),
        }
        if self.user_id:
            context_dict['user_id'] = self.user_id
        if self.snapshot_timestamp:
            context_dict['snapshot_timestamp'] = \
                self.snapshot_timestamp.float_timestamp

        return context_dict

    @classmethod
    def deserialize(cls, context_dict):
        snapshot_timestamp = arrow.get(context_dict['snapshot_timestamp']) \
            if 'snapshot_timestamp' in context_dict else None
        return cls(
            user_id=context_dict.get('user_id'),
            snapshot_timestamp=snapshot_timestamp,
            data_dir=context_dict['data_dir'],
        )
