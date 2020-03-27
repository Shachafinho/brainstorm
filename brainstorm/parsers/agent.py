from .bound_parser import bind_parse
from .parser import Parser


def _create_publishing_bound_parse(mq, bound_parse, output_topic):
    def _publishing_parse(serialized_message):
        result = bound_parse(serialized_message)
        if output_topic:
            mq.publish(result, topic=output_topic)
    return _publishing_parse


class Agent:
    def __init__(self, mq, parser):
        self._parser = parser
        self._mq = mq

        for input_topic, output_topic in parser.bindings:
            self.bind(input_topic, output_topic)

    def bind(self, input_topic, output_topic):
        bound_parse = bind_parse(self._parser, input_topic, output_topic)
        publishing_bound_parse = _create_publishing_bound_parse(
            self._mq, bound_parse, output_topic)
        self._mq.subscribe(publishing_bound_parse, topic=input_topic)

    def run(self):
        self._mq.consume_forever()

    @classmethod
    def from_parser_name(cls, mq, parser_name):
        return cls(mq, Parser(parser_name))
