import pathlib
import os

from brainstorm import __file__ as root_file


ROOT_DIR = pathlib.Path(root_file).parent.absolute()


def path_to_package(path):
    """Transform a path to a dotted name notation.

    Args:
        path (str): The path to transform.

    Return:
        str: The path in a dotted name notation.
    """
    return str(path).replace(os.path.sep, '.')
