class BankAccount(object):
    def __init__(self, name, balance, currency):
        self.name = name
        self.balance = balance
        self.currency = currency

        # # self.history1 = []
        # self.history1 = self.history1.append("Account was created")
        # self.history1 = self.history1.append("Deposited {} {}")

    def __int__(self):
        return self.balance

    def __str__(self):
        return "Bank account for {} with balance of {} {}.".format(self.name, self.balance, self.currency)

    def withdraw(self, money):
        if self.balance >= money:
            self.balance -= money
            return True
        return False

    def history(self):
        self.history1 = self.history1.append("Balance check -> {} {}".format(self.balance, self.currency))
        self.history1 = self.history1.append("__int__ check -> {} {}".format(self.balance, self.currency))
        return self.history1
