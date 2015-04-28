import requests
import copy


class Strings:
    FOLLOWERS = "https://api.github.com/users/{}/followers?client_id=926275e6df122f430b26&client_secret=9fcec76b0044441be11969aa391a217a3f87018c"
    USER = "https://api.github.com/users/{}?client_id=926275e6df122f430b26&client_secret=9fcec76b0044441be11969aa391a217a3f87018c"
    PRINT_FOLLOWERS = "The followers of {} are {}"
    PRINT_FOLLOWING = "The user {} follows {}"
    LOGIN = "login"
    BLOG = "blog"
    EMAIL = "email"


class DirectGraph():

    def __init__(self, userName):
        self.name = userName
        self.ListOfVisitedUsers = []
        self.data = {}

    def get_data_type(self, dataType):

        for user in self.ListOfVisitedUsers:
            userNameUrl = requests.get(self.make_url(user))
            userNameJson = userNameUrl.json()
            try:
                dataItem = userNameJson[dataType]
            except Exception:
                pass
            if dataItem != "":
                self.data[user] = dataItem

    def make_url(self, userName):
        return Strings.USER.format(userName)

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

    def get_followers(self, userName):
        userNameUrl = requests.get(self.make_url_followers(userName))
        userNameJson = userNameUrl.json()
        userNameFollowers = [followers[Strings.LOGIN]
                             for followers in userNameJson]
        return userNameFollowers

    def make_url_followers(self, userName):
        return Strings.FOLLOWERS.format(userName)


def startMe():
    user = "vitosh"
    graph = DirectGraph(user)
    graph.build_network(user, 3)
    graph.get_data_type(Strings.BLOG)

    with open('blog.txt', 'w') as outfile:
        working_file = graph.data.values()
        myLength, currentNumber = len(working_file), 0
        for address in working_file:
            if (address):
                outfile.write("{}\n".format(address))
                print("{0:.0%}".format(currentNumber / myLength))
            currentNumber += 1
        outfile.close
    print("Finished")
if __name__ == '__main__':
    startMe()
