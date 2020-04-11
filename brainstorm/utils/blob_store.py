import pathlib
import tempfile


class BlobStore:
    def __init__(self, data_dir):
        self.data_dir = pathlib.Path(str(data_dir))

    def _path_to_relative_path(self, path):
        return pathlib.Path(str(path)).relative_to(self.data_dir)

    def _path_to_token(self, path):
        return str(self._path_to_relative_path(path))

    def _relative_path_to_path(self, relative_path):
        return self.data_dir / relative_path

    def _token_to_path(self, token):
        return self._relative_path_to_path(token)

    def _path(self, suffix=None, prefix=None, subdir=None):
        subdir = subdir or ''
        dir_path = self.data_dir / subdir
        dir_path.mkdir(mode=0o775, parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
                suffix=suffix, prefix=prefix, dir=dir_path, delete=False) as f:
            return pathlib.Path(f.name)

    def load(self, token):
        file_path = self._token_to_path(token)
        return file_path.read_bytes()

    def save(self, data, suffix=None, prefix=None, subdir=None):
        file_path = self._path(suffix, prefix, subdir)
        file_path.write_bytes(data)
        return self._path_to_token(file_path)

    def remove(self, token):
        file_path = self._token_to_path(token)
        file_path.unlink()
