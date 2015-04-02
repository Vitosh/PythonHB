import unittest
from w3a import BankAccount


class Checker(unittest.TestCase):

    def setUp(self):
        self.test_acc = BankAccount("Vitosh", 100, "BGL")
        print(BankAccount.history())
        print("Check")

    def tearDown(self):
        pass

    def test_constructor_takes_name(self):
        cAccount = self.test_acc
        self.assertTrue(isinstance(cAccount, BankAccount))

    def test_try_to_stringify_the_class(self):
        cAccount = self.test_acc
        self.assertEqual
        (str(cAccount), "Bank account for Vitosh with balance of 100 BGL.")

    def test_check_the_bankAccount_to_integer(self):
        cAccount = self.test_acc
        self.assertEqual(int(cAccount), 100)

    def test_check_withdraw_balance(self):
        cAccount = self.test_acc
        self.assertTrue(cAccount.withdraw(50))

    def test_check_balance_functions(self):
        cAccount = self.test_acc
        cAccount.withdraw(40)
        self.assertTrue(cAccount.balance == 60)

    # def test_create_account_history(self):
    #     cAccount = self.test_acc
    #     self.assertEqual(cAccount.history(), ['Account was created', 'Deposited 1000$', 'Balance check -> 1000$', '__int__ check -> 1000$']))

if __name__ == '__main__':
    unittest.main()