import importlib
import inspect
import pathlib
import sys

from brainstorm.drivers.driver_manager import DriverManager


_READER_CLASS_NAME = 'Reader'
_READER_MODULE_NAME = 'reader'
_FORMATS_DIR = pathlib.Path(__file__).parent.parent.absolute() / 'formats'
_FORMATS_DIR_STR = str(_FORMATS_DIR)


def _find_reader_in_module(module):
    reader = module.__dict__.get(_READER_CLASS_NAME)
    if reader is not None and inspect.isclass(reader):
        return reader
    raise LookupError()


def find_reader(reader_tag):
    # Load the reader corresponding with the given tag.
    try:
        if _FORMATS_DIR_STR not in sys.path:
            sys.path.insert(0, _FORMATS_DIR_STR)
        reader_module = importlib.import_module(
            f'{reader_tag}.{_READER_MODULE_NAME}', package=reader_tag)

        return _find_reader_in_module(reader_module)
    except (ImportError, LookupError, ModuleNotFoundError):
        raise ValueError(f'Unsupported format for reader: {reader_tag!r}')


reader_manager = DriverManager(find_reader)


if __name__ == '__main__':
    for tag in ['binary', 'protobuf', 'unknown']:
        print(f'Attempting to find {tag!r} reader')
        binary_reader = reader_manager.find_driver(tag)
        print(f'Found {tag!r} reader')
