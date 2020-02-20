class Translation:
    __slots__ = 'x', 'y', 'z'

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'x={self.x}, y={self.y}, z={self.z})')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.x == other.x and
                self.y == other.y and
                self.z == other.z)
