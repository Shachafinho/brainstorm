import gzip
import pathlib


_FILE_FORMATS = {
    '.gz': gzip.open,
}


def get_opener(path):
    path = pathlib.Path(path)
    return _FILE_FORMATS.get(path.suffix, open)
