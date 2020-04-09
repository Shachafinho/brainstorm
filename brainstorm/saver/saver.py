import functools
import pathlib

from brainstorm.database import Database
from brainstorm.utils.drivers import ExhaustiveConfig
from brainstorm.utils.drivers import ExhaustiveDriverManager
from brainstorm.utils.drivers.exhaustive_driver_manager import \
    extract_class_driver, extract_func_driver, extract_module_drivers


TAG_FIELD = 'topic'


class_driver_extractor = functools.partial(
    extract_class_driver, name_pattern=r'.*Saver')

func_driver_extractor = functools.partial(
    extract_func_driver, name_pattern=r'save(_.+)?')

module_drivers_extractor = functools.partial(
    extract_module_drivers, tag_field=TAG_FIELD, driver_extractors=[
        class_driver_extractor, func_driver_extractor])

saver_manager = ExhaustiveDriverManager(ExhaustiveConfig(
    search_dir=pathlib.Path(__file__).parent.absolute() / 'savers',
    module_drivers_extractor=module_drivers_extractor))


class Saver:
    def __init__(self, url):
        self._database = Database(url)

    def save(self, topic, data):
        saver = saver_manager.find_driver(topic)
        saver(self._database, data)

    def __enter__(self):
        self._database.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return self._database.__exit__(exc_type, exc_value, exc_traceback)

    @property
    def topics(self):
        return saver_manager.drivers.keys()
