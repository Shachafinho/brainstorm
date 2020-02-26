import importlib
import inspect

from brainstorm.drivers.driver_manager import DriverManager


class HandlerConfig:
    __slots__ = 'module_name', 'class_name'

    def __init__(self, module_name, class_name):
        self.module_name = module_name
        self.class_name = class_name


_CONFIG = {
    'read': HandlerConfig(module_name='reader', class_name='Reader'),
    'write': HandlerConfig(module_name='writer', class_name='Writer'),
}


def _find_handler_in_module(module, target):
    handler_class_name = _CONFIG[target].class_name
    handler = module.__dict__.get(handler_class_name)
    if inspect.isclass(handler):
        return handler
    raise LookupError(
        f'Failed to locate {handler_class_name!r} class in module {module!r}')


def _find_handler(format_tag, target):
    try:
        handler_module_name = _CONFIG[target].module_name
        handler_module = importlib.import_module(
            f'.{handler_module_name}', package=f'{__package__}.{format_tag}')

        return _find_handler_in_module(handler_module, target)
    except (ImportError, LookupError, ModuleNotFoundError):
        raise ValueError(f'Unsupported format for {target!r}: {format_tag!r}')


def _find_reader(format_tag):
    return _find_handler(format_tag, 'read')


def _find_writer(format_tag):
    return _find_handler(format_tag, 'write')


reader_manager = DriverManager(_find_reader)
writer_manager = DriverManager(_find_writer)


if __name__ == '__main__':
    for tag in ['binary', 'protobuf', 'unknown']:
        print(f'Attempting to find {tag!r} reader')
        reader = reader_manager.find_driver(tag)
        print(f'Found {tag!r} reader: {reader!r}')
