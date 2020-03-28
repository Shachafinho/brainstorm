class DriverManager:
    def __init__(self, find_driver, drivers=None):
        self._find_driver = find_driver
        self.drivers = {} if drivers is None else drivers

    def find_driver(self, driver_tag):
        if driver_tag not in self.drivers:
            self.drivers[driver_tag] = self._find_driver(driver_tag)
        return self.drivers[driver_tag]
