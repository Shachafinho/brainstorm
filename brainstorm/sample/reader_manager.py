import importlib
import inspect
import pathlib
import sys


READER_CLASS_NAME = 'Reader'


def _find_reader_in_module(module):
    reader = module.__dict__.get(READER_CLASS_NAME)
    if reader is not None and inspect.isclass(reader):
        return reader
    raise LookupError()


class ReaderManager:
    def __init__(self, readers=None):
        self.readers = readers or {}

    def find_reader(self, file_path):
        file_path = pathlib.Path(file_path)
        extension = ''.join(file_path.suffixes)
        reader_tag = extension.replace('.', '_')
        if reader_tag in self.readers:
            return self.readers[reader_tag]

        # Load the reader corresponding with the required extension.
        try:
            current_dir = pathlib.Path(__file__).parent.absolute()
            sys.path.insert(0, str(current_dir))
            reader_module = importlib.import_module(
                f'{reader_tag}.reader', package=reader_tag)

            reader_class = _find_reader_in_module(reader_module)
            self.readers[reader_tag] = reader_class
            return reader_class
        except (ImportError, LookupError, ModuleNotFoundError):
            raise ValueError(f'Unsupported file format: {extension!r}')


reader_manager = ReaderManager()


if __name__ == '__main__':
    samples_dir = pathlib.Path('/home/user/Downloads/')

    print('Attempting to find .mind reader')
    mind_reader = reader_manager.find_reader(samples_dir / 'sample.mind')
    print('Found .mind reader')

    print('Attempting to find .mind reader')
    mind_gz_reader = reader_manager.find_reader(samples_dir / 'sample.mind.gz')
    print('Found .mind.gz reader')

    print('Attempting to find .unknown reader')
    unknown_reader = reader_manager.find_reader(samples_dir / 'sample.unknown')
    print('Found .unknown reader')
