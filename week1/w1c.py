import sys
import math
from copy import *


def count_words(arr):
    dResult = dict((i, arr.count(i)) for i in arr)

    return dResult


def unique_words_count(arr):
    iResult = 0
    iResult = len(count_words(arr))

    return iResult


def nan_expand(times):
    sResult = ""
    if times == 0:
        return sResult

    sNot = "Not a "
    sNaN = "NaN"

    for i in range(0, times):
        sResult += sNot
    sResult += sNaN

    return sResult


def iterations_of_nan_expand(expanded):

    iResult = expanded.count("Not a ")
    if expanded != nan_expand(iResult):
        return False

    return iResult


def group(example=[]):
    lResult3

    return lResult3


def take_same(lInput=[]):
    lResult4 = []
    z = 0

    while(len(lInput) > z-1):
        lResult4[z] = lInput[z]
        if lInput[z] != lInput[z+1]:
            break
        z+=1

    return lResult4
