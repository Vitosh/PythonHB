import json


class FootballTeam:

    def __init__(self):
        self._teamList = {}

    def add_to_team(self, player):
        self._teamList[player] = [player._salary]

    def change_team_list(self, dict):
        self._teamList = {}
        self._teamList = dict

    def show_team(self):
        return self._teamList


class FootballPlayer:
    def __init__(self, name, age, salary):
        self._name = name
        self._age = age
        self._salary = salary

    def __str__(self):
        return self._name + " " + str(self._age)

    def __repr__(self):
        return str(self)

    def salary(self, player):
        return str(player._salary)

AFC_Lions = FootballTeam()

player1 = FootballPlayer("Ivan", 22, 15000)
player2 = FootballPlayer("Stoyan", 23, 16000)
player3 = FootballPlayer("Damyan", 25, 17000)
player4 = FootballPlayer("Kaloyan", 19, 18000)
print(player1)

AFC_Lions.add_to_team(player1)
AFC_Lions.add_to_team(player2)
AFC_Lions.add_to_team(player3)
AFC_Lions.add_to_team(player4)
print(AFC_Lions.show_team())

with open('exported.txt', 'w') as outfile:
    json.dump(str(AFC_Lions.show_team()), outfile)
print("\nPrinting to file is ready!")

print("Now load:")
ownfile = open("imported.txt", "r")
data = ownfile.read()
print("Raw data from the file:\n", data)
print("Data to json:\n", json.loads(data), "\n")
print("Replacing the new data and showing:")
AFC_Lions.change_team_list(json.loads(data))
print(AFC_Lions.show_team())
