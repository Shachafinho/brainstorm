from .parser import Parser
from brainstorm.message_queue import Topic


def bind_parse(parser, input_topic=None, output_topic=None):
    # Use default topics if none were provided, otherwise use them as-is.
    # Note that invalid topics may cause errors.
    if not input_topic and not output_topic:
        input_topic, output_topic = parser.bindings[0]

    def _bound_parse(serialized_message):
        # Empty output topic discards the result.
        context, message = Topic(input_topic).deserialize(serialized_message)
        result = parser(context, message)
        return Topic(output_topic).serialize(context, result) \
            if output_topic else ''
    return _bound_parse


def parse(parser_name, data, input_topic=None, output_topic=None):
    bound_parse = bind_parse(Parser(parser_name), input_topic, output_topic)
    return bound_parse(data)
