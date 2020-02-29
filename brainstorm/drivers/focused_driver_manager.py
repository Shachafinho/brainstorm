import functools
import importlib
import inspect
import os
import pathlib

from .driver_manager import DriverManager
from .utils import path_to_package
from .utils import ROOT_DIR


class FocusedConfig:
    __slots__ = 'search_dir', 'module_name', 'class_name'

    def __init__(self, search_dir, module_name, class_name):
        self.search_dir = pathlib.Path(str(search_dir))
        self.module_name = module_name
        self.class_name = class_name


def _find_driver_in_module(module, config):
    driver = module.__dict__.get(config.class_name)
    if inspect.isclass(driver):
        return driver
    raise LookupError(
        f'Failed to locate {config.class_name!r} class in module {module!r}')


def _find_focused_driver(tag, config):
    try:
        relative_search_dir = config.search_dir.relative_to(ROOT_DIR.parent)
        search_package = path_to_package(relative_search_dir)
        driver_module = importlib.import_module(
            f'.{config.module_name}', package=f'{search_package}.{tag}')

        return _find_driver_in_module(driver_module, config)
    except (ImportError, LookupError, ModuleNotFoundError):
        raise ValueError(f'Unsupported driver for {tag!r}')


class FocusedDriverManager:
    def __init__(self, config, drivers=None):
        find_driver = functools.partial(_find_focused_driver, config=config)
        self._driver_manager = DriverManager(find_driver, drivers)

    def find_driver(self, driver_tag):
        return self._driver_manager.find_driver(driver_tag)
