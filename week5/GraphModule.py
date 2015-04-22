import requests


class DirectGraph():

    def __init__(self, url):

        self.r = requests.get(url)
        self.status_code = self.r.status_code
        self.headers = self.r.headers
        self.text = self.r.text
        self.json = self.r.json()

        self.followers = [a["login"] for a in self.json]
        print(self.followers)

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


def startMe():
    graph = DirectGraph("https://api.github.com/users/vitosh/followers")
    print(graph)

if __name__ == '__main__':
    startMe()


# TODO
# Graph&Test
# Build graph through GitHub
# Console if for asking
