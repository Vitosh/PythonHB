import unittest
from panda.py import *


class Checker(unittest.TestCase):

    def test_checkPanda(self):
        newPanda = Panda("Peter", "peter@panda.bg", "Male")
        self.assertTrue(isinstance(Panda, newPanda))

if __name__ == '__main__':
    unittest.main()
