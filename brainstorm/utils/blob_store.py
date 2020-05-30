import pathlib
import tempfile


class BlobStore:
    """An object responsible for loading and storing data.
    """

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
        """Return the data associated with the specified token.

        Args:
            token (str): Some key associated with stored data.

        Return:
            bytes: The data associated with the specified token.
        """
        file_path = self._token_to_path(token)
        return file_path.read_bytes()

    def save(self, data, suffix=None, prefix=None, subdir=None):
        """Store the specified data and return an associated token.

        Args:
            data (bytes): The data to store.
            suffix (str): Suffix for the file in which the data is stored.
            prefix (str): Prefix for the file in which the data is stored.
            subdir (str): Subdirectory for the file in which the data is
              stored.

        Return:
            str: The token associated with the stored data.
        """
        file_path = self._path(suffix, prefix, subdir)
        file_path.write_bytes(data)
        return self._path_to_token(file_path)

    def remove(self, token):
        """Remove the data associated with the specified token.

        Args:
            token (str): Some key associated with the stored data.
        """
        file_path = self._token_to_path(token)
        file_path.unlink()
