import pathlib
import os

from brainstorm import __file__ as root_file


ROOT_DIR = pathlib.Path(root_file).parent.absolute()


def path_to_package(path):
    return str(path).replace(os.path.sep, '.')
