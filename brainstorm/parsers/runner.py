from .parser_manager import parser_manager


def parse(parser_name, data):
    parser = parser_manager.find_driver(parser_name)
    return parser(data)
