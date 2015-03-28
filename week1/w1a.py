def sum(xs):
    result = 0
    for x in xs:
        result += x
    return result


def factorial(number):

    product = 1
    for i in range(number):
        product = product*(i+1)
    return product


def fibonacci(n):
    result = []
    a = 1
    b = 1

    while len(result) != n:
        result.append(a)
        next_fib = a+b
        a = b
        b = next_fib

    return result


def fibonacci2(n):
    a, b = 1, 1
    s = "["

    for i in range(n):
        s += str(a) + ", "
        a, b = b, a+b
    s = s[:-2]
    s += "]"
    return s


def sum_of_digits(n):

    if int(n) < 0:
        n = n * (-1)

    myResult = 0
    text = str(n)

    for digit in text:
        myResult = int(digit) + myResult

    return myResult

def fact_digits(n):
    myResult = 0
    text = str(n)
    for digit in text:
        myResult += factorial(int(digit))
    return myResult

def palindrome(obj):
    if isinstance(obj, int):
        obj = str(obj)

    if str(obj[::-1]) == str(obj):
        myResult = True
    else:
        myResult = False

    return myResult

def fibonacci(n):
    result = []
    a = 1
    b = 1

    while len(result) != n:
        result.append(a)
        next_fib = a+b
        a = b
        b = next_fib

    return result

def to_digits(n):
    result = []

    a = str(n)
    for x in a:
        result.append(x)

    return result

def fib_number_length(n):
    return len(str(fibonacci(n)))



def to_number(digits=[]):
    myResult =""
    for x in digits:
        myResult += str(x)
    return myResult


def fib_number(n):
    strResult = ""

    for i in range(1 , n+1):
        strResult += str(fibonacci_exact(i))
    intResult = int(strResult)
    return intResult

def fibonacci_exact(n):
    a = 1
    b = 1
    m = 1
    result = 1

    while m != n:
        result = b
        next_fib = a+b
        a = b
        b = next_fib
        m+=1
    return result

def count_vowels(myStr):
    counter = 0
    myStr = str(myStr)
    for i in myStr:
        if i in ["a","e","i","o","u","y"]:
            counter+=1
    return counter

def count_consonants(myStr):
    counter = 0
    myStr = str(myStr)
    for i in myStr:
        if i not in ["a","e","i","o","u","y"]:
            counter+=1
    return counter

def char_histogram(strInput):
    myDictionary = {}

    for i in strInput:
        myDictionary[i]= strInput.count(i)
    return myDictionary

#question - why does it work like this?
#print(char_histogram("AAAAaaa!!!"))
#print(char_histogram("Python!"))

def p_sconre(n):

    if palindrome(n):
        return 1
    iResult = 1

    while not palindrome(n):
        m = str(n)[::-1] #reverse n with this one
        iResult+=1
        n=n+int(m)

    return iResult


def is_increasing(seq=[]):
    bResult = True
    bIsFirst = True

    for x in seq:
        if bIsFirst == True:
            bIsFirst = False
            iCompareWith = x
            continue

        if iCompareWith >= x:
            bResult = False
    return bResult

def is_decreasing(seq=[]):
    bResult = True
    bIsFirst = True

    for x in seq:
        if bIsFirst == True:
            bIsFirst = False
            iCompareWith = x
            continue

        if iCompareWith <= x:
            bResult = False
    return bResult

def dec_to_bin(x):
    return int(bin(x)[2:])

def count_ones(x):
    m = str(x)
    bResult = False
    z = 0
    for i in m:
        if i == "1":
            z+=1

    if z%2>0:
        bResult = True

    return bResult

def next_hack(n):
    m=n+1

    while (not count_ones(dec_to_bin(m))) or (not palindrome(dec_to_bin(m))):
        m+=1
    return m
