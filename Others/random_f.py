import random


def print_list(myResults, myList):
    total_percentage = 0
    for x in range(0, len(myResults)):
        if myResults[x]:
            print("{} -> {}".format(x + 1, myResults[x]))

            percentage = 100 * ((x + 1) * myResults[x]) / len(myList)
            total_percentage += percentage

            print("{} %".format(round(percentage, 2)))
    print("Grand total percentage {}!".format(round(total_percentage, 2)))


def simple_print(myList):
    for x in range(0, len(myList)):
        print("{}".format(myList[x]))


myList = []
myResults = [0] * 100

generatedRandom = -1
previous = 0
countMatch = 0

for x in range(0, 10):
    if x > 0:
        previous = generatedRandom
    generatedRandom = random.randint(1, 6)

    if generatedRandom == previous:
        countMatch += 1
        if countMatch > 1:
            myResults[countMatch - 1] = myResults[countMatch - 1] - 1
            myResults[countMatch] = myResults[countMatch] + 1
        else:
            myResults[countMatch] = myResults[countMatch] + 1
    else:
        countMatch = 0
    myList.append(generatedRandom)


simple_print(myList)
print("Matches:")
print_list(myResults, myList)
