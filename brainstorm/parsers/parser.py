import functools
import pathlib

from brainstorm.utils.drivers import ExhaustiveConfig
from brainstorm.utils.drivers import ExhaustiveDriverManager
from brainstorm.utils.drivers.exhaustive_driver_manager import \
    extract_class_driver, extract_func_driver, extract_module_drivers


TAG_FIELD = 'tag'
"""The field name for the parser tag (parser name)."""


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
    """A manager object to choose and relay a specific parser implementation.

    Each specific parser is ONLY responsible for manipulating an
    :mod:`MQ object <brainstorm.message_queue.objects>`.

    Parsers are uniquely identified using the
    :const:`~brainstorm.parsers.parser.TAG_FIELD` field.

    Serialization and deserialization are done in
    :class:`~brainstorm.message_queue.Topic`.
    """

    BINDINGS_FIELD = 'bindings'
    """The field name for the parser bindings."""

    def __init__(self, parser_name):
        """Construct a Parser manager object.

        Args:
            parser_name (str): The name of the specific parser.
        """
        self._parser_driver = parser_manager.find_driver(parser_name)

    def __call__(self, context, mq_obj):
        """Parse the MQ object using the specified *context*.

        Args:
            context (:class:`~brainstorm.message_queue.Context`):
              A context object which holds convenient information.
            mq_obj: The MQ object to parse.

        Return:
            tuple(:class:`~brainstorm.message_queue.Context`, object):
              The parser result object, together with the context used.
        """
        return self._parser_driver(context, mq_obj)

    @property
    def bindings(self):
        """The parser (*input_topic*, *output_topic*) bindings.

        Each parser may accept its input from some *input_topic*, and may emit
        its results to some *output_topic*.

        A parser can explicitly specify its bindings using the field
        :const:`~brainstorm.parsers.Parser.BINDING_FIELD`

        If the field is not specified, it is assumed the parser emits its
        results to the :const:`~brainstorm.parsers.parser.TAG_FIELD` topic,
        as well as having no input topic.

        Return:
            tuple(str, str): The parser bindings.
        """
        if hasattr(self._parser_driver, self.BINDINGS_FIELD):
            return getattr(self._parser_driver, self.BINDINGS_FIELD)

        return (None, getattr(self._parser_driver, TAG_FIELD))


if __name__ == '__main__':
    # TODO: Remove
    for parser in parser_manager._driver_manager._drivers.values():
        print(repr(parser))
