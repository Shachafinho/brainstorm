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
        if extension in self.readers:
            return self.readers[extension]

        # Load the reader corresponding with the required extension.
        try:
            current_dir = pathlib.Path(__file__).parent.absolute()
            sys.path.insert(0, str(current_dir))
            reader_module = importlib.import_module(
                f'{extension[1:]}.reader', package=extension)

            reader_class = _find_reader_in_module(reader_module)
            self.readers[extension] = reader_class
            return reader_class
        except (ImportError, LookupError) as e:
            print(e)
            raise ValueError(f'Unsupported format: {extension!r}')


reader_manager = ReaderManager()


if __name__ == '__main__':
    samples_dir = pathlib.Path('/home/user/Downloads/')
    mind_reader = reader_manager.find_reader(samples_dir / 'sample.mind')
    mind_gz_reader = reader_manager.find_reader(samples_dir / 'sample.mind.gz')
    unknown_reader = reader_manager.find_reader(samples_dir / 'sample.unknown')
