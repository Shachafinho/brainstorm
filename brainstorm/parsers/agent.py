from .bound_parser import BoundParser
from .parser import Parser


def _create_publishing_bound_parse(mq, bound_parse, output_topic):
    def _publishing_parse(serialized_message):
        result = bound_parse(serialized_message)
        if output_topic:
            mq.publish(result, topic=output_topic)
    return _publishing_parse


class Agent:
    """An object responsible for running parsers on some message queue.
    """

    def __init__(self, mq, parsers=None):
        """Construct an Agent object.

        Args:
            mq (:class:`~brainstorm.message_queue.MessageQueue`):
              A message queue object to operate on.
            parsers (list(:class:`~brainstorm.parsers.Parser`)):
              A collection of parsers to be run.
        """
        self._mq = mq
        self._parsers = []

        parsers = parsers or []
        for parser in parsers:
            self.bind(parser)

    def bind(self, parser):
        """Register a parser to be run on the message queue.

        Args:
            parser (:class:`~brainstorm.parsers.Parser`): The parser to
              be registered and run.
        """
        bound_parser = BoundParser(parser)
        publishing_bound_parse = _create_publishing_bound_parse(
            self._mq, bound_parser, bound_parser.output_topic)
        self._mq.subscribe(publishing_bound_parse,
                           topic=bound_parser.input_topic)
        self._parsers.append(parser)

    def run(self):
        """Run all registered parsers on the message queue.
        """
        self._mq.consume_forever()

    @classmethod
    def from_parsers_names(cls, mq, parsers_names):
        """Construct an agent object from a collection of parser names.

        Args:
            mq (:class:`~brainstorm.message_queue.MessageQueue`):
              A message queue object to operate on.
            parsers_names (list(str)):
              A collection of parser names to be run.

        Return:
            :class:`~brainstorm.parser.Agent`:
              The constructed agent object.
        """
        return cls(mq, map(Parser, parsers_names))
