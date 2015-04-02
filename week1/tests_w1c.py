import unittest
from w1a import *


class Checker(unittest.TestCase):

    # def setUp(self):
    #     self.test_acc = BankAccount("Vitosh", 100, "BGL")
    #     print(BankAccount.history())
    #     print("Check")

    # def tearDown(self):
    #     pass

    def test_sum_XS(self):
        self.assertTrue(sum([5, 5]) == 10)

    def test_factorial(self):
        self.assertTrue(factorial(5) == 1*2*3*4*5)

    def test_fibonacci(self):
        self.assertEqual(fibonacci(5), [1, 1, 2, 3, 5])

    def test_fibonacci2(self):
        self.assertEqual(fibonacci2(5), "[1, 1, 2, 3, 5]")

    def test_sum_of_digits(self):
        self.assertEqual(sum_of_digits(5556), 21)

    def test_fact_digits(self):
        self.assertEqual(fact_digits(55), 240)

    def test_to_digits(self):
        self.assertEqual(to_digits("100"), ['1', '0', '0'])

    def test_fib_number_len(self):
        self.assertEqual(fib_number_length(5), 15)

    def test_count_volwes(self):
        self.assertEqual(count_vowels("Vitosh"), 2)

    def test_count_consonants(self):
        self.assertEqual(count_consonants("Vitosh"), 4)

    def test_char_histogram(self):
        self.assertEqual(char_histogram("555"), {'5': 3})

    def test_is_increasing(self):
        self.assertEqual(is_increasing([5, 6, 7]), True)

    def test_is_increasing(self):
        self.assertFalse(is_increasing([5, 6, 7, 8, -5]))


if __name__ == '__main__':
    unittest.main()
