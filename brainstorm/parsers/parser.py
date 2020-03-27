import functools
import pathlib

from brainstorm.utils.drivers import ExhaustiveConfig
from brainstorm.utils.drivers import ExhaustiveDriverManager
from brainstorm.utils.drivers.exhaustive_driver_manager import \
    extract_class_driver, extract_func_driver, extract_module_drivers


TAG_FIELD = 'tag'
BINDINGS_FIELD = 'bindings'


class_driver_extractor = functools.partial(
    extract_class_driver, name_pattern=r'.*Parser')

func_driver_extractor = functools.partial(
    extract_func_driver, name_pattern=r'parse(_.+)?')

module_drivers_extractor = functools.partial(
    extract_module_drivers, tag_field=TAG_FIELD, driver_extractors=[
        class_driver_extractor, func_driver_extractor])

parser_manager = ExhaustiveDriverManager(ExhaustiveConfig(
    search_dir=pathlib.Path(__file__).parent.absolute() / 'parsers',
    module_drivers_extractor=module_drivers_extractor))


class Parser:
    def __init__(self, parser_name):
        self._parser_driver = parser_manager.find_driver(parser_name)

    def __call__(self, context, message):
        return self._parser_driver(context, message)

    @property
    def bindings(self):
        if hasattr(self._parser_driver, BINDINGS_FIELD):
            return getattr(self._parser_driver, BINDINGS_FIELD)

        return [(None, getattr(self._parser_driver, TAG_FIELD))]


if __name__ == '__main__':
    # TODO: Remove
    for parser in parser_manager._driver_manager._drivers.values():
        print(repr(parser))
