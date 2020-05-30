from .parser import Parser
from brainstorm.message_queue import Topic


class BoundParser:
    """A wrapper object binding a parser to its input and output topics.
    """

    def __init__(self, parser):
        """Constructs a BoundParser object for the specified parser.

        Args:
            parser (:class:`~brainstorm.parsers.Parser`): The parser to bind.
        """
        self._parser = parser
        self._input_topic = None
        self._output_topic = None

    @property
    def input_topic(self):
        """The bound parser's input topic.

        Return:
            str: The bound parser's input topic.
        """
        if not self._input_topic:
            self._input_topic = self._parser.bindings[0]
        return self._input_topic

    @property
    def output_topic(self):
        """The bound parser's output topic.

        Return:
            str: The bound parser's output topic.
        """
        if not self._output_topic:
            self._output_topic = self._parser.bindings[1]
        return self._output_topic

    def __call__(self, serialized_mq_obj):
        """Deserialze, parse and then serialize the given serialized MQ object.

        Use the wrapped parser to parse the MQ object.
        Since both the MQ object and the parsed results are serialized, use the
        output (input) topic to deserialize (re-serialize) the input (result).

        Args:
            serialized_mq_obj (bytes): The serialized input MQ object to parse.

        Return:
            bytes: Serialized result.
        """
        context, mq_obj = \
            Topic(self.input_topic).deserialize(serialized_mq_obj)
        context, result_obj = self._parser(context, mq_obj)
        return Topic(self.output_topic).serialize(context, result_obj) \
            if self.output_topic else (context, result_obj)


def parse(parser_name, data):
    """Parse the given data using the parser of the specified name.

    Accept a parser name and some data, as consumed from the message queue.
    Use the specific parser to parse the data, and return the results, as
    published to the message queue.

    Args:
        parser_name (str): The name of the parser to be used.
        data (bytes): The (serialized) data to parse, as consumed from the
          message queue.

    Return:
        bytes: The serialized result, as published to the message queue.
    """
    bound_parser = BoundParser(Parser(parser_name))
    return bound_parser(data)
