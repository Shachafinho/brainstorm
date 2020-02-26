import contextlib
import importlib
import inspect

from brainstorm.drivers.driver_manager import DriverManager


class HandlerConfig:
    __slots__ = 'module_name', 'class_name'

    def __init__(self, module_name, class_name):
        self.module_name = module_name
        self.class_name = class_name


class FormatterDriver:
    __slots__ = 'reader', 'writer'

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    def __repr__(self):
        args = ', '.join([f'{k}={getattr(self, k)!r}' for k in self.__slots__])
        return f'{self.__class__.__name__}({args})'


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


def find_handler(format_tag, target):
    try:
        handler_module_name = _CONFIG[target].module_name
        handler_module = importlib.import_module(
            f'.{handler_module_name}', package=f'{__package__}.{format_tag}')

        return _find_handler_in_module(handler_module, target)
    except (ImportError, LookupError, ModuleNotFoundError):
        raise ValueError(f'Unsupported format for {target!r}: {format_tag!r}')


def find_driver(format_tag):
    reader = None
    with contextlib.suppress(ValueError):
        reader = find_handler(format_tag, 'read')
    writer = None
    with contextlib.suppress(ValueError):
        writer = find_handler(format_tag, 'write')

    if reader is None and writer is None:
        raise ValueError(f'Unsupported format: {format_tag!r}')

    return FormatterDriver(reader, writer)


formatter_manager = DriverManager(find_driver)


if __name__ == '__main__':
    for tag in ['binary', 'protobuf', 'unknown']:
        print(f'Attempting to find {tag!r} reader')
        driver = formatter_manager.find_driver(tag)
        print(f'Found {tag!r} driver: {driver!r}')
