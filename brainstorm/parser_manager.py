import importlib
import inspect
import pathlib
import re
import sys


class ParserManager:
    TAG_FIELD = 'tag'
    CLASS_REGEX = r'.*Parser'
    CLASS_PARSE_METHOD = 'parse'
    FUNCTION_REGEX = r'parse_.+'

    def __init__(self, parsers=None):
        self.parsers = parsers or {}

    @classmethod
    def from_parser_dirs(cls, *parsers_dirs):
        parser_manager = cls()
        for parsers_dir in parsers_dirs:
            parser_manager.load_parsers(parsers_dir)
        return parser_manager

    def get_parser_tags(self):
        return self.parsers.keys()

    def parse(self, context, snapshot):
        for parser in self.parsers.values():
            parser(context, snapshot)

    def _get_parser_tag(self, parser):
        return getattr(parser, self.TAG_FIELD, None)

    def _load_class_parser(self, parser):
        tag = self._get_parser_tag(parser)
        if not tag or not re.match(self.CLASS_REGEX, parser.__name__):
            return

        if not hasattr(parser, self.CLASS_PARSE_METHOD):
            # TODO: issue a warning
            # print(f'Class {parser.__name__} doesn\'t implement '
            #       f'{self.CLASS_PARSE_METHOD!r} method')
            return

        self.parsers[tag] = getattr(parser(), self.CLASS_PARSE_METHOD)

    def _load_function_parser(self, parser):
        tag = self._get_parser_tag(parser)
        if not tag or not re.match(self.FUNCTION_REGEX, parser.__name__):
            return

        self.parsers[tag] = parser

    def _load_parsers_from_module(self, module):
        for obj in module.__dict__.values():
            if inspect.isclass(obj):
                self._load_class_parser(obj)
            elif inspect.isroutine(obj):
                self._load_function_parser(obj)

    def load_parsers(self, parsers_dir):
        parsers_dir = pathlib.Path(parsers_dir)
        sys.path.insert(0, str(parsers_dir.parent))
        for path in parsers_dir.iterdir():
            if path.name.startswith('_') or path.suffix != '.py':
                continue

            module = importlib.import_module(
                f'{parsers_dir.name}.{path.stem}', package=parsers_dir.name)
            self._load_parsers_from_module(module)


if __name__ == '__main__':
    # TODO: Remove
    from brainstorm.protocol import Snapshot
    snapshot = Snapshot()

    parsers_dir = (pathlib.Path(__file__).parent / 'parsers').absolute()
    parser_manager = ParserManager()
    parser_manager.load_parsers(parsers_dir)
    parser_manager.parse(None, snapshot)
