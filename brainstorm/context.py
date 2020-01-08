import pathlib


class Context:
    def __init__(self, data_dir, user_id, snapshot_timestamp):
        self.data_dir = data_dir
        self.user_id = user_id
        self.timestamp = snapshot_timestamp

    def path(self, filename, *, create_dirs=True):
        timestamp_str = self.timestamp.format('YYYY-MM-DD_HH-mm-ss-SSSSSS')
        file_path = pathlib.Path(
            self.data_dir, str(self.user_id), timestamp_str, filename)

        # Create directories along the path (as needed).
        if create_dirs:
            file_path.parent.mkdir(mode=0o775, parents=True, exist_ok=True)
        return file_path

    def save(self, filename, data):
        self.path(filename).write_bytes(data)
