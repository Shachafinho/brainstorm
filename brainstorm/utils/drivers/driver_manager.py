class DriverManager:
    """An object responsible for locating drivers (handlers).
    """

    def __init__(self, find_driver, drivers=None):
        """Construct a DriverManager object.

        Args:
            find_driver (func(str)): A lookup function to return a driver
              object based on its name.
            drivers (dict): A mapping of drivers' names to their respective
              objects.
        """
        self._find_driver = find_driver
        self.drivers = {} if drivers is None else drivers

    def find_driver(self, driver_tag):
        """Return the driver corresponding to the given tag.

        Args:
            driver_tag (str): The tag (name) of the driver to search for.

        Return:
            object: Driver object corresponding to the given tag.
        """
        if driver_tag not in self.drivers:
            self.drivers[driver_tag] = self._find_driver(driver_tag)
        return self.drivers[driver_tag]
