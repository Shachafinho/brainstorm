import importlib
import inspect
import pathlib
import sys

from brainstorm.drivers.driver_manager import DriverManager


class FormatterDriver:
    __slots__ = 'reader', 'writer'

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer


_CONFIG = {
    'read': ('Reader', 'reader'),
    'write': ('Writer', 'writer'),
}


_FORMATS_DIR = pathlib.Path(__file__).parent.absolute() / 'formats'
_FORMATS_DIR_STR = str(_FORMATS_DIR)


def _find_class_in_module(module):
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


def find_driver(format_tag):
    reader = find_handler('read', format_tag)
    writer = find_handler('write', format_tag)
    return FormatterDriver(reader, writer)


reader_manager = DriverManager(functools.partial(find_formatter, 'reader'))
writer_manager = DriverManager(functools.partial(find_formatter, 'writer'))


if __name__ == '__main__':
    for tag in ['binary', 'protobuf', 'unknown']:
        print(f'Attempting to find {tag!r} reader')
        binary_reader = reader_manager.find_driver(tag)
        print(f'Found {tag!r} reader')
