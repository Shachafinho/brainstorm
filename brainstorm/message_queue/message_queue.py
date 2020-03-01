from furl import furl

from brainstorm.utils.drivers import FocusedConfig
from brainstorm.utils.drivers import FocusedDriverManager


mq_manager = FocusedDriverManager(FocusedConfig(
    search_dir=pathlib.Path(__file__).parent.absolute(),
    module_name='handler',
    class_name='Handler',
))


class MessageQueue:
    def __init__(self, url):
        url = furl(url)
        driver_cls = mq_manager.find_driver(url.scheme)
        self._driver = driver_cls(url.netloc)

    def publish(self, queue_id, message):
        self._driver.publish(queue_id, message)

    def consume(self, queue_id, callback):
        self._driver.consume(queue_id, callback)
