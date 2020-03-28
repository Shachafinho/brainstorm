import pathlib

from arrow import Arrow

from brainstorm.utils.paths import ROOT_DIR


DEFAULT_DATA_DIR = ROOT_DIR.parent / 'data'
TIMESTAMP_FORMAT = 'YYYY-MM-DD_HH-mm-ss-SSSSSS'


class Context:
    def __init__(self, user_id, snapshot_timestamp=None, data_dir=None):
        self.user_id = user_id
        self.timestamp = snapshot_timestamp
        self.data_dir = pathlib.Path(data_dir) if data_dir is not None \
            else DEFAULT_DATA_DIR

    def path(self, filename, *, create_dirs=True):
        timestamp = self.timestamp.format(TIMESTAMP_FORMAT) \
            if self.timestamp is not None else ''
        file_path = self.data_dir / str(self.user_id) / timestamp / filename

        # Create directories along the path (as needed).
        if create_dirs:
            file_path.parent.mkdir(mode=0o775, parents=True, exist_ok=True)
        return file_path

    def save(self, filename, data):
        self.path(filename).write_bytes(data)

    def serialize(self):
        context_dict =  {
            'user_id': self.user_id,
            'data_dir': str(self.data_dir),
        }
        if self.timestamp:
            context_dict['timestamp'] = self.timestamp.float_timestamp

        return context_dict

    @classmethod
    def deserialize(cls, context_dict):
        timestamp = Arrow.utcfromtimestamp(context_dict['timestamp']) \
            if 'timestamp' in context_dict else None
        return cls(
            user_id=context_dict['user_id'],
            snapshot_timestamp=timestamp,
            data_dir=context_dict['data_dir'],
        )
