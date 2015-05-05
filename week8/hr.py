import json

myFile = open("students.json", "r")
jsonText = json.loads(myFile.read())
myListOfStudents = [student["name"] for student in jsonText]


def generate_data_student_table():
    myStudentList = []

    for student in jsonText:
        for course in student["courses"]:
            empty = []
            myStudentList.append(empty)
            empty.append(student["name"])
            if student["github"] == "" or student["github"] == None:
                student["github"] = "No Git"
            empty.append(student["github"])
            empty.append(course["name"])

    return myStudentList


def get_student_to_github():
    myDictionary = {}

    for student in myListOfStudents:
        gitAccount = get_github_account(student)
        if not gitAccount:
            gitAccount = "No github available."
        myDictionary[student] = gitAccount
    return myDictionary


def get_github_account(student):
    for value in jsonText:
        if value["name"] == student:
            return value["github"]


def get_courses(student):
    courses = set()
    for value in jsonText:
        if value["name"] == student:
            for course in value["courses"]:
                courses.add(course["name"])
    return courses


def get_all_courses():
    courses = set()
    for value in jsonText:
        for course in value["courses"]:
            courses.add(course["name"])
    return courses

# a = generate_data_student_table()
# print(*a, sep='\n')
# print(mySet[0])
# print(mySet[1])
# print(mySet[2])

# get_courses("Vitosh Doynov")

# for student in myListOfStudents:
#     myGithub = get_github_account(student)
#     myCourses = get_courses(student)


# print(get_github_account("Vitosh Doynov"))

# class D():

#     def __init__(self):
#         self.name = userName
#         self.GeneralDictionary = {}
#         self.ListOfVisitedUsers = []

#     def build_network_with_followers(self):

#         self.GeneralDictionary = {}
#         while len(self.ListOfVisitedUsers) > 0:
#             nextUser = (self.ListOfVisitedUsers).pop(0)
#             nextUserFollowers = self.get_followers(nextUser)
#             self.GeneralDictionary[nextUser] = nextUserFollowers
#         return self.GeneralDictionary

#     def build_network(self, user, level):

#         self.ListOfVisitedUsers = []
#         visited = set()
#         myQ = []

#         visited.add(user)
#         myQ.append(user)

#         while level > 0:
#             print("Level {} consists of {}".format(level, len(myQ)))
#             while len(myQ):
#                 nextUser = myQ.pop(0)
#                 n 
# extUserFollowers = self.get_followers(nextUser)

#                 for newUser in nextUserFollowers:
#                     if newUser not in visited:
#                         visited |= {newUser}
#                         self.ListOfVisitedUsers.append(newUser)

#             myQ = copy.deepcopy(self.ListOfVisitedUsers)

#             level -= 1
#         return self.ListOfVisitedUsers

#     def print_dictionary(self):
#         for key in sorted(self.GeneralDictionary):
#             print("{} : {}".format(key, self.GeneralDictionary[key]))

#     def get_followers(self, userName):

#     def add_edge(self, node_a, node_b):
#         self.GeneralDictionary[node_a] = node_b

#     def get_neighbours_for(self, node):
#         return self.GeneralDictionary[node]

#     def make_url_followers(self, userName):
#         return Strings.FOLLOWERS.format(userName)

# def startMe():
#     user = "vitosh"
#     graph = DirectGraph(user)
#     graph.build_network(user, 3)
#     graph.build_network_with_followers()
#     graph.print_dictionary()

# if __name__ == '__main__':
#     startMe()
