from .parser_manager import Parser


def _create_process_func(mq, parser, output_topic=None):
    def _process(message):
        result = parser(message)
        if output_topic is not None:
            mq.publish(result, topic=output_topic)
    return _process


class Agent:
    def __init__(self, mq, parser):
        self._parser = parser
        self._mq = mq
        self._processors = {}

        for input_topic, output_topic in parser.bindings:
            self.bind(input_topic, output_topic=output_topic)

    def _get_processor(self, output_topic=None):
        if output_topic not in self._processors:
            self._processors[output_topic] = _create_process_func(
                self._mq, self._parser, output_topic=output_topic)
        return self._processors[output_topic]

    def bind(self, input_topic, output_topic=None):
        processor = self._get_processor(output_topic=output_topic)
        self._mq.subscribe(processor, topic=input_topic)

    def run(self):
        self._mq.consume_forever()

    @classmethod
    def from_parser_name(cls, mq, parser_name):
        return cls(mq, Parser(parser_name))
