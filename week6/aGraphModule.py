import requests


class Strings:
    FOLLOWERS = "https://api.github.com/users/{}/followers?client_id=926275e6df122f430b26&client_secret=9fcec76b0044441be11969aa391a217a3f87018c"
    FOLLOWING = "https://api.github.com/users/{}/following?client_id=926275e6df122f430b26&client_secret=9fcec76b0044441be11969aa391a217a3f87018c"
    PRINT_FOLLOWERS = "The followers of {} are {}"
    PRINT_FOLLOWING = "The user {} follows {}"


class DirectGraph():

    def __init__(self, userName):
        self.name = userName

        # Followers
        self.rFollowers = requests.get(self.make_url_followers(userName))
        self.jsonFollowers = self.rFollowers.json()
        self.Followers = [followers["login"]for followers in self.jsonFollowers]

    def print_followers(self):
        print(Strings.PRINT_FOLLOWERS.format(self.name, self.Followers))

    def make_url_followers(self, userName):
        return Strings.FOLLOWERS.format(userName)

    def generate_hell_of_followers(self, count):
        for someFollower in self.Followers:
            someFollowerURL = requests.get(self.make_url_followers(someFollower))
            someFollowerJSON = someFollowerURL.json()
            someFollowerFollowers = [followers["login"]for followers in someFollowerJSON]

            for someFollower2 in someFollowerFollowers:

                if (someFollower2 not in self.Followers):
                    self.Followers.append(someFollower2)
                    count -= 1

            if count == 0:
                return

def startMe():
    user = "vitosh"
    graph = DirectGraph(user)
    graph.generate_hell_of_followers(300)
    sortedList = sorted(graph.Followers)
    print("\n".join(sortedList))

if __name__ == '__main__':
    startMe()