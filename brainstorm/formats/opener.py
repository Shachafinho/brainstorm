import gzip
import pathlib


_FILE_FORMATS = {
    '.gz': gzip.open,
}


def get_opener(path):
    """Return the appropriate open function for the specified path.

    Args:
        path (str): A path to some file.

    Return:
        func(str):
          A function which opens the specified path and returns a file-like
          object.
    """
    path = pathlib.Path(path)
    return _FILE_FORMATS.get(path.suffix, open)
