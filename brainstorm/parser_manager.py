import pathlib

from brainstorm.utils.drivers import ExhaustiveConfig
from brainstorm.utils.drivers import ExhaustiveDriverManager


parser_manager = ExhaustiveDriverManager(ExhaustiveConfig(
    search_dir=(pathlib.Path(__file__).parent / 'parsers').absolute(),
    class_regex=r'.*Parser',
    needed_class_method='parse',
    func_regex=r'parse(_.+)?'
))


if __name__ == '__main__':
    # TODO: Remove
    for parser in parser_manager._driver_manager._drivers.values():
        print(repr(parser))
