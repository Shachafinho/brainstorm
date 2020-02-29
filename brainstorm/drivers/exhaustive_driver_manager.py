import functools
import importlib
import inspect
import pathlib
import re

from .driver_manager import DriverManager
from .utils import path_to_package
from .utils import ROOT_DIR


class ExhaustiveConfig:
    __slots__ = 'search_dir', 'module_pattern', 'tag_field', \
                'class_regex', 'needed_class_method', 'func_regex'

    def __init__(self, search_dir, module_pattern=None, tag_field=None,
                 class_regex=None, needed_class_method=None, func_regex=None):
        self.search_dir = pathlib.Path(str(search_dir))

        # The following mustn't be empty.
        self.module_pattern = module_pattern or '[!_]*.py'
        self.tag_field = tag_field or 'tag'

        # The following are allowed to be empty.
        self.class_regex = r'.*' if class_regex is None else class_regex
        self.needed_class_method = 'handle' if needed_class_method is None \
            else needed_class_method
        self.func_regex = r'.*' if func_regex is None else func_regex


def _is_class_driver(obj, config):
    return inspect.isclass(obj) and \
        re.match(config.class_regex, obj.__name__) and \
        hasattr(obj, config.needed_class_method)


def _get_class_driver(cls, config):
    return getattr(cls(), config.needed_class_method)


def _is_function_driver(obj, config):
    return inspect.isroutine(obj) and \
        re.match(config.func_regex, obj.__name__)


def _get_function_driver(func):
    return func


def _find_drivers_in_module(module, config):
    drivers = {}
    for obj in module.__dict__.values():
        tag = getattr(obj, config.tag_field, None)
        if tag is None:
            continue

        if _is_class_driver(obj, config):
            drivers[tag] = _get_class_driver(obj, config)
        elif _is_function_driver(obj, config):
            drivers[tag] = _get_function_driver(obj)

    return drivers


def _find_all_drivers(config):
    drivers = {}
    for path in config.search_dir.rglob(config.module_pattern):
        package = path_to_package(path.parent.relative_to(ROOT_DIR.parent))
        driver_module = importlib.import_module(
            f'.{path.stem}', package=package)
        drivers.update(_find_drivers_in_module(driver_module, config))
    return drivers


def _erronous_find_driver(driver_tag):
    raise KeyError(driver_tag)


class ExhaustiveDriverManager:
    def __init__(self, config, drivers=None):
        drivers = _find_all_drivers(config) if drivers is None else drivers
        self._driver_manager = DriverManager(_erronous_find_driver, drivers)

    def find_driver(self, driver_tag):
        return self._driver_manager.find_driver(driver_tag)
