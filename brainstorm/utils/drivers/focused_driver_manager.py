import functools
import importlib
import inspect
import os
import pathlib

from .driver_manager import DriverManager
from brainstorm.utils.paths import path_to_package
from brainstorm.utils.paths import ROOT_DIR


class DirectoryFocusedConfig:
    __slots__ = 'search_dir', 'module_name', 'class_name'

    def __init__(self, search_dir, module_name, class_name):
        self.search_dir = pathlib.Path(str(search_dir))
        self.module_name = module_name
        self.class_name = class_name

    def import_module(self, tag, search_package):
        return importlib.import_module(
            f'.{self.module_name}', package=f'{search_package}.{tag}')

    def find_driver_in_module(self, module):
        driver = module.__dict__.get(self.class_name)
        if inspect.isclass(driver):
            return driver
        raise LookupError(
            f'Failed to locate {self.class_name!r} class in module {module!r}')


class ModuleFocusedConfig:
    __slots__ = 'search_dir'

    def __init__(self, search_dir):
        self.search_dir = pathlib.Path(str(search_dir))

    def import_module(self, tag, search_package):
        return importlib.import_module(f'.{tag}', package=search_package)

    def find_driver_in_module(self, module):
        return module


def _find_focused_driver(tag, config):
    try:
        relative_search_dir = config.search_dir.relative_to(ROOT_DIR.parent)
        search_package = path_to_package(relative_search_dir)
        driver_module = config.import_module(tag, search_package)
        return config.find_driver_in_module(driver_module)
    except (ImportError, LookupError, ModuleNotFoundError):
        raise ValueError(f'Unsupported driver for {tag!r}')


class FocusedDriverManager:
    def __init__(self, config, drivers=None):
        find_driver = functools.partial(_find_focused_driver, config=config)
        self._driver_manager = DriverManager(find_driver, drivers)

    @property
    def drivers(self):
        return self._driver_manager.drivers

    @drivers.setter
    def drivers(self, drivers):
        self._driver_manager.drivers = drivers

    def find_driver(self, driver_tag):
        return self._driver_manager.find_driver(driver_tag)
