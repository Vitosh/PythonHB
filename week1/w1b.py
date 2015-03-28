import math

def sum_of_divisors(n):
    z = 1
    iResult = 0

    while z<=n:
        if n/z == int(n/z):
            iResult+=z
        z+=1

    return iResult

def is_prime(n):
    bResult = False

    if sum_of_divisors(n) == n+1:
        bResult = True

    return bResult


def prime_number_of_divisors(n):
    z=1
    iResult = 0

    while z<=n:
        if n/z == int(n/z):
            iResult+=1
        z+=1

    bResult = is_prime(iResult)

    return bResult


def contains_digit(number, digit):
    bResult = False

    iSum = sum([1 for x in to_digits(str(number))])
    if iSum == digit:
        bResult = True

    return bResult


def to_digits(n):
    return [int(x) for x in str(n)]


def contains_digits(number,digits=[]):

    bResult = True
    sNumber = str(number)

    for item in digits:
        sItem = str(item)

        #print(item)
        #print(sNumber.find(sItem))

        if sNumber.find(sItem) == -1:
            bResult = False
            return bResult

    return bResult




def is_number_balanced(n):
    bResult = False
    sN = str(n)

    sLeft,sRight = sN[:len(sN)//2],sN[len(sN)//2:]

    iLeft = sum(int(x) for x in sLeft)
    iRight = sum(int(x) for x in sRight)

    bResult = (iLeft == iRight)

    return bResult
   

def count_substrings(haystack,needle):
    iResult = 0
    iResult = haystack.count(needle)
    return iResult

def zero_insert(n):
    iResult = 0
    
    sN = str(n)
    x = 0
    sMirror = sN
    iCount = 1

    while x < len(sN)-1:
        if ((sN[x] == sN[x+1]) or calculate_10(sN[x],sN[x+1])):
            
            sMirror = insert_zero(sMirror,x+iCount)
            iCount +=1
            
        x+=1

    iResult = int(sMirror)
    return iResult

def insert_zero(string, index):
    return string[:index] + '0' + string[index:]

def calculate_10(first,second):
    bResult = False

    iFirst = int(first)
    iSecond  = int(second)
    
    if (iFirst+iSecond)%10 == 0:
        bResult = True
    return bResult



def sum_matrix(m=[]):
    a = sum([sum(o) for o in m])
    return a
    
    
m = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
#print(sum_matrix(m))

m = {(0, 0): 1,
     (0, 1): 2,
     (0, 2): 3,
     (1, 0): 4,
     (1, 1): 5,
     (1, 2): 6,
     (2, 0): 7,
     (2, 1): 8,
     (2, 2): 9
     }    

def zero_if_negative(myValue):
    if myValue<1:
        return 0
    return myValue

def matrix_bombing_plan(myValue):    
    lResult = dict(myValue)
    
    #define greatest k[0] iGreatest0
    #define greatest k[1] iGreatest1
    iGreatestRow = 0
    iGreatestCol = 0
    
    for k in iter(myValue.keys()):
        if iGreatestRow < k[0]:
            iGreatestRow = k[0]
        if iGreatestCol < k[1]:
            iGreatestCol = k[1]
    
    for k in iter(myValue.keys()):
        iRow = k[0]
        iCol = k[1]      
                
        #Rebuilding the dictionary here:
        lTempResult = dict(myValue)
        
        #Left, Right, Up and Down:
        if iRow+1<=iGreatestRow:
            lTempResult[iRow+1,iCol]-=lTempResult[iRow,iCol]
            
        if iRow-1>=0:
            lTempResult[iRow-1,iCol]-=lTempResult[iRow,iCol]
            
        if iCol+1<=iGreatestCol:
            lTempResult[iRow,iCol+1]-=lTempResult[iRow,iCol]
            
        if iCol-1>=0:
            lTempResult[iRow,iCol-1]-=lTempResult[iRow,iCol]
        
        #Diagonals:
        if iCol-1>=0 and iRow-1>=0:
            lTempResult[iRow-1,iCol-1]-=lTempResult[iRow,iCol]
            
        if iCol+1<=iGreatestCol and iRow-1>=0:
            lTempResult[iRow-1,iCol+1]-=lTempResult[iRow,iCol]
                        
        if iCol-1>=0 and iRow+1<=iGreatestRow:
            lTempResult[iRow+1,iCol-1]-=lTempResult[iRow,iCol]
            
        if iCol+1<=iGreatestCol and iRow+1<=iGreatestRow:
            lTempResult[iRow+1,iCol+1]-=lTempResult[iRow,iCol]

        for key in lTempResult:
            if lTempResult[key]<0:
                lTempResult[key]=0      
                
        lResult[iRow,iCol]=sum(lTempResult.values())
        
    return lResult

print(matrix_bombing_plan(m))