import sys
import os
from random import randint


def main():
    for arg in sys.argv[1:]:
        filename = arg
        file = open(filename, "r")
        content = file.read()
        print(content)
        file.close


def GenerateRandoms(n):
    sRandoms = ""
    i = 0
    while i < n:
        sRandoms += str(randint(1, 1000)) + " "
        i += 1
    sRandoms.strip

    return sRandoms


def randomNumbers():
    filename = sys.argv[1]
    file = open(filename, "w")
    contents = GenerateRandoms(int(sys.argv[2]))
    file.write(contents)
    file.close


def calculate():
    filename = sys.argv[1]
    file = open(filename, "r")
    content = file.read()
    file.close

    myList = list()
    myList = content.split()
    myList = [int(i) for i in myList]

    print(sum(myList))


def fileSize():
    try:
        total_size = os.path.getsize(sys.argv[1])
        print(total_size, " bits", sys.argv[1])

    except OSError:
        print("Error -> File name not correct")


if __name__ == '__main__':
    calculate()
