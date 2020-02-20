class UserInformation:
    __slots__ = 'user_id', 'name', 'birth_date', 'gender'

    def __init__(self, user_id, name, birth_date, gender):
        self.user_id = user_id
        self.name = name
        self.birth_date = birth_date
        self.gender = gender

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'user_id={self.user_id}, name={self.name}, '
                f'birth_date={self.birth_date}, gender={self.gender})')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.user_id == other.user_id and
                self.name == other.name and
                self.birth_date == other.birth_date and
                self.gender == other.gender)
