def is_an_bn(word):
    iLen = len(word)//2

    if len(word) % 2 == 1:
        return False

    a = word[:iLen]
    b = word[iLen:]

    if(a == "a"*iLen)and(b == "b"*iLen):
        return True

    return False


def is_credit_card_valid(number):
    if number % 2 == 0:
        return False

    sNumber = str(number)
    sNumber = [int(x)*2 for x in sNumber if int(x) % 2 == 1]

    iNumber = sum([int(x) for x in sNumber])
    if iNumber % 10 == 0:
        return True

    return False

# print(is_credit_card_valid(79927398713))
# print(is_credit_card_valid(79927398715))


def is_prime(n):

    if n == 1:
        return False

    z = 2

    while z < n:
        if divide_count(n, z) > 0:
            return False
        z += 1
    return True


def divide_count(n, k):
    times = 0

    while n % k == 0:
        times += 1
        n = n/k

    return times


def goldbach(n):
    lResult = []
    iCounter = 2

    while(iCounter < (n//2)+1):
        if is_prime(iCounter):
            if is_prime(n-iCounter):
                lResult.append((iCounter, n-iCounter))
        iCounter += 1

    return lResult


print(goldbach(100))
print(goldbach(200))
