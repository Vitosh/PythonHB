import requests
import copy


class Strings:
    FOLLOWERS = "https://api.github.com/users/{}/followers?client_id=926275e6df122f430b26&client_secret=9fcec76b0044441be11969aa391a217a3f87018c"
    PRINT_FOLLOWERS = "The followers of {} are {}"
    PRINT_FOLLOWING = "The user {} follows {}"
    LOGIN = "login"
    BLOG = "blog"
    EMAIL = "email"


class DirectGraph():

    def __init__(self, userName):
        self.name = userName
        self.GeneralDictionary = {}
        self.ListOfVisitedUsers = []

    def get_data_type(self, dataType):
        data = {}

        for user in self.ListOfVisitedUsers:
            data[user] = self.get_data(user, dataType)
        return data

    def build_network_with_followers(self):

        self.GeneralDictionary = {}
        while len(self.ListOfVisitedUsers) > 0:
            nextUser = (self.ListOfVisitedUsers).pop(0)
            nextUserFollowers = self.get_followers(nextUser)
            self.GeneralDictionary[nextUser] = nextUserFollowers
        return self.GeneralDictionary

    def build_network(self, user, level):

        self.ListOfVisitedUsers = []
        visited = set()
        myQ = []

        visited.add(user)
        myQ.append(user)

        while level > 0:
            print("Level {} consists of {}".format(level, len(myQ)))
            while len(myQ):
                nextUser = myQ.pop(0)
                nextUserFollowers = self.get_followers(nextUser)

                for newUser in nextUserFollowers:
                    if newUser not in visited:
                        visited |= {newUser}
                        self.ListOfVisitedUsers.append(newUser)

            myQ = copy.deepcopy(self.ListOfVisitedUsers)

            level -= 1
        return self.ListOfVisitedUsers

    def print_dictionary(self):
        for key in sorted(self.GeneralDictionary):
            print("{} : {}".format(key, self.GeneralDictionary[key]))

    def get_data(self, userName, dataType):
        userNameUrl = requests.get(self.make_url_followers(userName))
        userNameJson = userNameUrl.json()
        userNameFollowers = [followers[dataType]for followers in userNameJson]
        return userNameFollowers

    def get_followers(self, userName):
        userNameUrl = requests.get(self.make_url_followers(userName))
        userNameJson = userNameUrl.json()
        userNameFollowers = [followers["login"]for followers in userNameJson]
        return userNameFollowers

    def add_edge(self, node_a, node_b):
        self.GeneralDictionary[node_a] = node_b

    def get_neighbours_for(self, node):
        return self.GeneralDictionary[node]

    def make_url_followers(self, userName):
        return Strings.FOLLOWERS.format(userName)


def startMe():
    user = "vitosh"
    graph = DirectGraph(user)
    graph.build_network(user, 2)
    print(graph.get_data_type(Strings.EMAIL))

if __name__ == '__main__':
    startMe()
