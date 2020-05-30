import importlib
import inspect
import pathlib
import re

from .driver_manager import DriverManager
from brainstorm.utils.paths import path_to_package
from brainstorm.utils.paths import ROOT_DIR


def extract_class_driver(obj, name_pattern=None):
    """Return a class-typed driver from the given object, if exists.

    Args:
        obj (object): An object to extract the driver from.
        name_pattern (str): A pattern against which the class name is matched.

    Return:
        None or object: The extracted driver, or None if none exists.
    """
    name_pattern = name_pattern or r'.*'

    if not inspect.isclass(obj):
        return None

    cls = obj
    if not re.match(name_pattern, cls.__name__):
        return None
    if '__call__' not in cls.__dict__:
        return None

    return cls()


def extract_func_driver(obj, name_pattern=None):
    """Return a func-typed driver from the given object, if exists.

    Args:
        obj (object): An object to extract the driver from.
        name_pattern (str): A pattern against which the function name is
          matched.

    Return:
        None or func: The extracted driver, or None if none exists.
    """
    name_pattern = name_pattern or r'.*'

    if not inspect.isroutine(obj):
        return None

    func = obj
    if not re.match(name_pattern, func.__name__):
        return None

    return func


def extract_module_drivers(module, tag_field=None, driver_extractors=None):
    """Return all drivers in the given module.

    Args:
        module (module): The module to be scanned for drivers.
        tag_field (str): The field name holding the driver tag (name).
        driver_extractors (list(func(object))): A collection of functions
          capable of extracting a driver function from an object.

    Return:
        dict(str, func):
          All drivers located inside the module.
    """
    tag_field = tag_field or 'tag'
    driver_extractors = driver_extractors or \
        [extract_class_driver, extract_func_driver]

    drivers = {}
    for obj in module.__dict__.values():
        tag = getattr(obj, tag_field, None)
        if tag is None:
            continue

        for extractor in driver_extractors:
            driver = extractor(obj)
            if driver is not None:
                drivers[tag] = driver

    return drivers


class ExhaustiveConfig:
    """An exhaustive configuration to locate drivers in a directory.
    """

    __slots__ = 'search_dir', 'module_pattern', 'module_drivers_extractor'

    def __init__(self, search_dir, module_pattern=None,
                 module_drivers_extractor=None):
        self.search_dir = pathlib.Path(str(search_dir))

        # The following mustn't be empty.
        self.module_pattern = module_pattern or '[!_]*.py'

        # The following are allowed to be empty.
        self.module_drivers_extractor = module_drivers_extractor or \
            extract_module_drivers


def _find_all_drivers(config):
    drivers = {}
    for path in config.search_dir.rglob(config.module_pattern):
        package = path_to_package(path.parent.relative_to(ROOT_DIR.parent))
        driver_module = importlib.import_module(
            f'.{path.stem}', package=package)
        drivers.update(config.module_drivers_extractor(driver_module))
    return drivers


def _erronous_find_driver(driver_tag):
    raise KeyError(f'Could not find {driver_tag!r} driver')


class ExhaustiveDriverManager:
    """A DriverManager using an exhaustive policy.

    Exhaustive policy dictates that drivers **cannot** be immediately found
    by their name. In other words, we have to (exhaustively) iterate over
    numerous possibilities until the desired driver is found.

    Each driver must still have its own unique tag/name.
    """

    def __init__(self, config, drivers=None):
        drivers = _find_all_drivers(config) if drivers is None else drivers
        self._driver_manager = DriverManager(_erronous_find_driver, drivers)

    @property
    def drivers(self):
        return self._driver_manager.drivers

    @drivers.setter
    def drivers(self, drivers):
        self._driver_manager.drivers = drivers

    def find_driver(self, driver_tag):
        return self._driver_manager.find_driver(driver_tag)
