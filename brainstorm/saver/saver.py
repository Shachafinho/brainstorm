import functools
import pathlib

from brainstorm.database import Database
from brainstorm.utils.drivers import ExhaustiveConfig
from brainstorm.utils.drivers import ExhaustiveDriverManager
from brainstorm.utils.drivers.exhaustive_driver_manager import \
    extract_class_driver, extract_func_driver, extract_module_drivers


TAG_FIELD = 'topic'
"""The field name for the saver tag (saver name)."""


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
    """A manager object to choose and relay a specific saver implementation.

    Each saver is associated with some topic, and are thus uniquely identified
    using the :const:`~brainstorm.saver.saver.TAG_FIELD` field.

    Each saver is responsible for deserializing its input, converting it to
    some :mod:`DB object <brainstorm.database.objects>`, and then store it in
    the DB.
    """

    def __init__(self, url):
        """Construct a Saver manager object.

        Args:
            url (str): A URL representing the specific database to use.
              The scheme determines the type of the database (e.g.
              *postgresql*), whereas the host and port determine the address of
              the database.
        """
        self._database = Database(url)

    def save(self, topic, data):
        """Save the data related to the given topic to the database.

        Args:
            topic (str): The name of the specific saver
              (the name of the topic it is associated with).
            data (bytes): The (serialized) data to save in the database,
              as consumed from the given topic.
        """
        saver = saver_manager.find_driver(topic)
        saver(self._database, data)

    def __enter__(self):
        self._database.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return self._database.__exit__(exc_type, exc_value, exc_traceback)

    @property
    def topics(self):
        """All supported topics for save.

        Return:
            list(str): All supported topics for save.
        """
        return saver_manager.drivers.keys()
