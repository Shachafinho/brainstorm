class Feelings:
    def __init__(self, hunger, thirst, exhaustion, happiness):
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'hunger={self.hunger}, thirst={self.thirst}, '
                f'exhaustion={self.exhaustion}, happiness={self.happiness})')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.hunger == other.hunger and
                self.thirst == other.thirst and
                self.exhaustion == other.exhaustion and
                self.happiness == other.happiness)
