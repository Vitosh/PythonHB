import unittest
from just2 import *


class Checker(unittest.TestCase):

    def setUp(self):
        self.panda1 = Panda("Peter", "p@pandamail.com", "male")
        self.panda2 = Panda("Georg", "g@pandamail.com", "male")
        self.panda3 = Panda("Teodo", "t@pandamail.com", "male")
        self.panda4 = Panda("Queen", "q@pandamail.com", "male")
        self.panda5 = Panda("Lilia", "l@pandamail.com", "female")
        self.panda6 = Panda("Romeo", "r@pandamail.com", "male")
        self.panda7 = Panda("Micha", "r@pandamail.com", "male")
        self.panda112 = Panda("ZZZZZ", "z@mail.com", "female")
        self.panda111 = Panda("OOOOOO", "O@mail.com", "female")

        self.network = PandaSocialNetwork()

        self.network.add_panda(panda112)
        self.network.add_panda(panda111)

        self.network.make_friends(panda112, panda111)
        self.network.make_friends(panda111, panda3)

        self.network.make_friends(panda1, panda2)
        self.network.make_friends(panda1, panda3)
        self.network.make_friends(panda2, panda5)
        self.network.make_friends(panda2, panda4)
        self.network.make_friends(panda4, panda6)
        self.network.make_friends(panda4, panda7)

    def test_check_name(self):
        self.assertEqual(self.panda1.name(), "Peter")

    def test_check_mail(self):
        self.assertEqual(self.panda1.email(), "p@pandamail.com")

    def test_checkGender(self):
        self.assertEqual(self.panda1.gender(), "male")

    def test_check_gender(self):
        self.assertEqual(self.panda1.isMale(), True)

    def test_check_gender_female(self):
        self.assertEqual(self.panda1.isFemale(), False)

    def test_str(self):
        self.assertEqual(self.panda1.__str__(), "Peter p@pandamail.com male")

    def test_compare(self):
        self.assertEqual(self.panda1.isFemale(), False)

    def test_check(self):
        self.assertTrue(self.panda1 != self.panda2)

if __name__ == '__main__':
    unittest.main()
