import re
import json


class PandaException(Exception):
    pass


class PandaAlreadyThere(PandaException):

    def __init__(self, value='PandaAlreadyThere'):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PandasAlreadyFriends(PandaException):

    def __init__(self, value='PandasAlreadyFriends'):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Panda:

    def __init__(self, name, email, gender):
        if not re.match(r'\w[\w\.-]*@\w[\w\.-]+\.\w+', email):
            print("Wrong email!")
            return
        if not (gender.lower() == 'male' or gender.lower() == 'female'):
            print("Wrong gender!")
            return
        self.__name = name
        self.__email = email
        self.__gender = gender.lower()

    def name(self):
        return self.__name

    def email(self):
        return self.__email

    def gender(self):
        return self.__gender

    def isMale(self):
        return self.__gender == 'male'

    def isFemale(self):
        return self.__gender == 'female'

    def __str__(self):
        return self.__name + " " + self.__email + " " + self.__gender

    def __repr__(self):
        return self.__name

    def __eq__(self, other):
        return (self.__name == other.name() and
                self.__email == other.email() and
                self.__gender == other.gender())

    def __hash__(self):
        return hash(self.__name + self.__email + self.__gender)


class PandaSocialNetwork:

    def __init__(self):
        self.__pandas = {}

    def pandas(self):
        return self.__pandas

    def change_value__pandas(self, dict):
        self.__pandas = {}
        print(dict)
        print("Here is printed!")
        self.__pandas = dict

    def add_panda(self, panda):
        if panda in self.__pandas:
            raise PandaAlreadyThere
        self.__pandas[panda] = []

    def has_panda(self, panda):
        return panda in self.__pandas

    def get_pandas(self):
        return self.__pandas

    def make_friends(self, other1, other2):
        if(other2 in self.__pandas.keys() and
           other1 in self.__pandas[other2]):
                raise PandasAlreadyFriends()
        if other1 in self.__pandas.keys():
            self.__pandas[other1].append(other2)
        else:
            self.__pandas[other1] = [other2]
        if other2 in self.__pandas.keys():
            self.__pandas[other2].append(other1)
        else:
            self.__pandas[other2] = [other1]

    def are_friends(self, other1, other2):
        return other2 in self.__pandas[other1]

    def friends_of(self, panda):
        if panda not in self.__pandas.keys():
            return False
        else:
            return self.__pandas[panda]

    def connection_level(self, panda1, panda2):
        if not (panda1 in self.__pandas.keys() and
                panda2 in self.__pandas.keys()):
            return False

        elif panda1 in self.__pandas[panda2]:
            return 1

        else:
            road_table = {}
            for panda in self.__pandas.keys():
                road_table[panda] = ""

            visited = [panda1]
            curr_panda = ""

            while visited != []:
                curr_panda = visited.pop(0)

                if curr_panda == panda2:
                    break

                else:
                    for PandaAfter in self.__pandas[curr_panda]:
                        if PandaAfter not in visited:
                            visited.append(PandaAfter)
                            if type(road_table[PandaAfter]) is str:
                                road_table[PandaAfter] = curr_panda
            road_len = 0
            start = panda2

            while start != panda1:
                road_len += 1
                start = road_table[start]

            return road_len

    def are_connected(self, panda1, panda2):
        return self.connection_level(panda1, panda2) != 0

    def how_many_gender_in_network(self, level, panda, gender):
        count = 0
        for next_panda in self.__pandas.keys():
            if next_panda != panda:
                if(self.connection_level(panda, next_panda) == level and
                   next_panda.gender() == gender):
                    count += 1
        return count


network = PandaSocialNetwork()

panda1 = Panda("Peter", "p@pandamail.com", "male")
panda2 = Panda("Georg", "g@pandamail.com", "male")
panda3 = Panda("Teodo", "t@pandamail.com", "male")
panda4 = Panda("Queen", "q@pandamail.com", "male")
panda5 = Panda("Lilia", "l@pandamail.com", "female")
panda6 = Panda("Romeo", "r@pandamail.com", "male")
panda7 = Panda("Micha", "r@pandamail.com", "male")

panda112 = Panda("ZZZZZ", "z@mail.com", "female")
panda111 = Panda("OOOOOO", "O@mail.com", "female")

network.add_panda(panda112)
network.add_panda(panda111)

network.make_friends(panda112, panda111)
network.make_friends(panda111, panda3)

network.make_friends(panda1, panda2)
network.make_friends(panda1, panda3)
network.make_friends(panda2, panda5)
network.make_friends(panda2, panda4)
network.make_friends(panda4, panda6)
network.make_friends(panda4, panda7)

print(network.pandas())
print(network.connection_level(panda1, panda5))
print(network.connection_level(panda112, panda6))
print(network.how_many_gender_in_network(1, panda1, 'male'))

with open('data.txt', 'w') as outfile:
    json.dump(str(network.pandas()), outfile)
print("Printing is ready!")
print("Now load\n")

ownfile = open("myfile.txt", "r")
data = ownfile.read()
print(data + "\n")
print(json.loads(data))

network.change_value__pandas(json.loads(data))
print(network.pandas())
