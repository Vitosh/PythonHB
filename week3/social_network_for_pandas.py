class Panda:

    def __init__(self, name, email, gender):
        self.name = name
        self.email = email
        self.gender = gender

    def isMale(self):
        if (self.gender == "male"):
            return True
        return False

    def isFemale(self):
        if (self.gender == "female"):
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


class PandaSocialNetwork:

    def __init__(self):
        self.social_network = {}

    def has_panda(self, panda):
        return panda in self.social_network

    def add_panda(self, panda):
        if self.has_panda(panda):
            raise Exception("Panda is already in the social network!")
        else:
            self.social_network[panda] = []

    def are_friends(self, panda1, panda2):
        return panda1 in self.social_network[panda2] and\
            panda2 in self.social_network[panda1]

    def make_friends(self, panda1, panda2):
        if not self.has_panda(panda1):
            self.add_panda(panda1)

        if not self.has_panda(panda2):
            self.add_panda(panda2)

        if self.are_friends(panda1, panda2):
            raise Exception("Pandas are already friends!")

        self.social_network[panda1] += panda2
        self.social_network[panda2] += panda1

    def friends_of(self, panda):
        if self.has_panda(panda):
            return self.social_network[panda]
        return False

    def conection_level(self, panda1, panda2):
        if self.has_panda(panda1) and self.has_panda(panda2):
            if self.are_friends(panda1, panda2):
                return 1
            # pass
            return -1
        return False

    # def are_concted(self, panda1, panda2):
    #    # ? if self.conecton_level(panda1, panda2) > 0

