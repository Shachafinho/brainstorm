import pathlib
import tempfile

from brainstorm.utils.paths import ROOT_DIR


DEFAULT_DATA_DIR = ROOT_DIR.parent / 'blobstore'


class BlobStore:
    def __init__(self, data_dir=None):
        self.data_dir = pathlib.Path(str(data_dir)) if data_dir is not None \
            else DEFAULT_DATA_DIR

    def _get_dir_path(self, subdir=None):
        subdir = subdir or ''
        return self.data_dir / subdir

    def path(self, suffix=None, prefix=None, subdir=None):
        dir_path = self._get_dir_path(subdir)
        dir_path.mkdir(mode=0o775, parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
                suffix=suffix, prefix=prefix, dir=dir_path, delete=False) as f:
            return f.name

    def load(self, filename, subdir=None):
        dir_path = self._get_dir_path(subdir)
        return (dir_path / filename).read_bytes()

    def save(self, filename, data, subdir=None):
        dir_path = self._get_dir_path(subdir)
        (dir_path / filename).write_bytes(data)
