class Pose:
    __slots__ = 'translation', 'rotation'

    def __init__(self, translation, rotation):
        self.translation = translation
        self.rotation = rotation

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'translation={self.translation}, rotation={self.rotation})')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.translation == other.translation and
                self.rotation == other.rotation)
