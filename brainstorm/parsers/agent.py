from .bound_parser import BoundParser
from .parser import Parser


def _create_publishing_bound_parse(mq, bound_parse, output_topic):
    def _publishing_parse(serialized_message):
        result = bound_parse(serialized_message)
        if output_topic:
            mq.publish(result, topic=output_topic)
    return _publishing_parse


class Agent:
    def __init__(self, mq, parsers=None):
        self._mq = mq
        self._parsers = []

        parsers = parsers or []
        for parser in parsers:
            self.bind(parser)

    def bind(self, parser):
        bound_parser = BoundParser(parser)
        publishing_bound_parse = _create_publishing_bound_parse(
            self._mq, bound_parser, bound_parser.output_topic)
        self._mq.subscribe(publishing_bound_parse,
                           topic=bound_parser.input_topic)
        self._parsers.append(parser)

    def run(self):
        self._mq.consume_forever()

    @classmethod
    def from_parsers_names(cls, mq, parsers_names):
        return cls(mq, map(Parser, parsers_names))
