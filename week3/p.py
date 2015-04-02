class Panda(object):

    def __init__(self, name, email, gender):
        self.name = name
        self.email = email
        self.gender = gender

    def isMale(self):
        if (self.gender == "Male"):
            return True
        return False

    def isFemale(self):
        if (self.gender == "Female"):
            return True
        return False

    def __str__(self):
        return '%s %s %s' % (self.name, self.email, self.gender)

    def __eq__(self, other):
        return (str(self) == str(other))

    def __hash__(self):
        return hash(self.__str__())

    def __repr__(self):
        return self.__str__


class SocialNetwork(object):

    def __init__():
        database = {}

    def has_panda(self, checkPanda):
        return checkPanda in self.database

    def add_panda(self, panda):
        if self.has_panda(panda):
            self.database[panda] = []
        else:
            raise Exception("PandasAlreadyExists")

