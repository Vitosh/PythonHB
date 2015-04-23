from collections import *

wordsInAnalysis = 310

myFile = open('textFile.txt')
text = [word.strip(",.\n?!:;[]()")
        for line in myFile for word in line.lower().split()]

words = [word for line in text for word in line.split()]


# print(Counter(words))
print("\n\n")

TopWordsNumber = 0

TopDictionary = Counter(words).most_common(wordsInAnalysis)
for i in TopDictionary:
    TopWordsNumber += int(words.count(i[0]))
    print(i)

TotalWords = len(words)
DiffWordsTotal = len(set(words))
PercentUniqueWordsOverAllUnique = int((wordsInAnalysis / DiffWordsTotal) * 100)
PercentUniqueWordsUsedInTime = int((TopWordsNumber / len(words)) * 100)


print("\n\nAnalysis: \n\n")
print("Words in total %s" % (TotalWords))
print("Different words in total: %s" % (DiffWordsTotal))
print("Words in top %s in total: %s" % (wordsInAnalysis, TopWordsNumber))
print("%s percent of the words are used in %s percent of the time in %s" % (
    PercentUniqueWordsOverAllUnique, PercentUniqueWordsUsedInTime, myFile.name))
print("\n\n")
