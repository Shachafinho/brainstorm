import pathlib

from brainstorm.utils.drivers import FocusedConfig
from brainstorm.utils.drivers import FocusedDriverManager


CURRENT_DIR = pathlib.Path(__file__).parent.absolute()


reader_manager = FocusedDriverManager(FocusedConfig(
    search_dir=CURRENT_DIR,
    module_name='reader',
    class_name='Reader',
))

writer_manager = FocusedDriverManager(FocusedConfig(
    search_dir=CURRENT_DIR,
    module_name='writer',
    class_name='Writer',
))


if __name__ == '__main__':
    for tag in ['binary', 'protobuf', 'unknown']:
        print(f'Attempting to find {tag!r} reader')
        reader = reader_manager.find_driver(tag)
        print(f'Found {tag!r} reader: {reader!r}')

        print(f'Attempting to find {tag!r} writer')
        writer = writer_manager.find_driver(tag)
        print(f'Found {tag!r} writer: {writer!r}')
