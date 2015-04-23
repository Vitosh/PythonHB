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
        self.Followers = [followers["login"]
                          for followers in self.jsonFollowers]

        self.EvenMoreFollowers = []
        self.EvenMoreFollowers.extend(self.Followers)

        # Following
        # self.rFollowing = requests.get(self.make_url_following(userName))
        # self.jsonFollowing = self.rFollowing.json()
        # self.Following = [following["login"]
        #                   for following in self.jsonFollowing]

        # self.followingSet = Set(self.Following)

    def print_followers(self):
        print(Strings.PRINT_FOLLOWERS.format(self.name, self.Followers))

    def print_following(self):
        print(Strings.PRINT_FOLLOWING.format(self.name, self.Following))

    def make_url_following(self, userName):
        return Strings.FOLLOWING.format(userName)

    def make_url_followers(self, userName):
        return Strings.FOLLOWERS.format(userName)

    # def generate_followers_of_followers(self, userName):
    #     for someFollower in self.Followers:
    #         someFollowerURL = requests.get(
    #             self.make_url_followers(someFollower))
    #         someFollowerJSON = someFollowerURL.json()
    #         someFollowerFollowers = [followers["login"]
    #                                  for followers in someFollowerJSON]

    #         self.followersSet.add(someFollowerFollowers)
    # print(Strings.PRINT_FOLLOWERS.format(
    # someFollower, someFollowerFollowers))

    def generate_hell_of_followers(self, count):
        for someFollower in self.EvenMoreFollowers:
            someFollowerURL = requests.get(
                self.make_url_followers(someFollower))
            someFollowerJSON = someFollowerURL.json()
            someFollowerFollowers = [followers["login"]
                                     for followers in someFollowerJSON]

            if (someFollowerFollowers not in self.EvenMoreFollowers):
                self.EvenMoreFollowers.extend(someFollowerFollowers)
            
            count -= 1
            if count == 0:
                return

    def add_edge(node_a, node_b):
        pass

    def get_neighbors_for(node):
        pass

    def path_between(node_a, node_b):
        pass

    def do_you_follow(user):
        pass

    def do_you_follow_indirectly(user):
        pass

    def does_he_she_follows(user):
        pass

    def does_he_she_follows_indirectly(user):
        pass

    def who_follows_you_back():
        pass

    def build_network(start, level):
        if level == 0:
            return
        # next_cycle = []
        # n = get_network_for(start)
        # for follower in n["follwers"]:
        #     self.g.add_edge(followers, start)

        # for following in n["following"]:
        #     g.add_edge(start, following)
        #     for next1 in next1.cycle:
        #         build_network(next, level - 1)

        # variant 2
        # visited = set()
        # q = []
        # visited.add(start)
        # q.append((0,start))
        # while q not empty:
        #     cl, cn = q.pop(0)
        #     for each (followed and not visited):
        #         visited.add each
        #         q.append((cl+1, each))

# "https://api.github.com/users/vitosh/followers"


def startMe():
    user = "vitosh"
    graph = DirectGraph(user)

    graph.generate_hell_of_followers(50)

    # print(graph.EvenMoreFollowers)
    sortedList = sorted(graph.EvenMoreFollowers)
    print("\n".join(sortedList))

if __name__ == '__main__':
    startMe()


# TODO
# Graph&Test
# Build graph through GitHub
# Console if for asking
