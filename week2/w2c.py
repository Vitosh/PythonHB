from decimal import *

class Bill:

    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return "A $ {} bill".format(self.amount)

    def __repr__(self):
        return self.__str__()

    def __int__(self):
        return self.amount

    def __eq__(self, other):
        return self.__int__() == other.__int__()

    def __hash__(self):
        return hash(self.__str__())


class BatchBill:
    def __init__(self, count):
        self.count = count

    def __len__(self):
        len(self.count)

    def __getitem__(self, index):
        return self.count[index]


class CashDesk:
    def __init__(self):
        self.total = 0
        self.bills = []

    def total(self):
        return sum([int(Bill) for Bill in self.bills])

    def inspect(self):
        pass

    def take_money(self, money):
        self.bills = money


class Fraction:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        return "{} / {}".format(self.numerator, self.denominator)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if other.denominator != other.denominator:
            return Fraction(self.numerator+other.numerator, self.denominator)
        newDenominator = other.denominator*self.denominator


    def __sub__(self, other):
        return Fraction(self.numerator - other.numerator, self.denominator - other.denominator)

    def __mul__(self, other):
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __eq__(self,other):
        return Decimal((self.numerator)/(self.denominator)) == Decimal((other.numerator)/(other.denominator))

a = Fraction(5,10)
b = Fraction(6,12)
c = Fraction(2,3)

d = a+b
print(d)
e = a-b
print(e)
f = a*b
print(f)
print(a == b)
