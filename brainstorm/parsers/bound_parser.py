from .parser import Parser
from brainstorm.message_queue import Topic


class BoundParser:
    def __init__(self, parser):
        self._parser = parser
        self._input_topic = None
        self._output_topic = None

    @property
    def input_topic(self):
        if not self._input_topic:
            self._input_topic = self._parser.bindings[0]
        return self._input_topic

    @property
    def output_topic(self):
        if not self._output_topic:
            self._output_topic = self._parser.bindings[1]
        return self._output_topic

    def __call__(self, serialized_mq_obj):
        context, mq_obj = \
            Topic(self.input_topic).deserialize(serialized_mq_obj)
        context, result_obj = self._parser(context, mq_obj)
        return Topic(self.output_topic).serialize(context, result_obj) \
            if self.output_topic else (context, result)


def parse(parser_name, data):
    bound_parser = BoundParser(Parser(parser_name))
    return bound_parser(data)
