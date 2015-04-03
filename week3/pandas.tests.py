import unittest
from pandas import *


class Checker(unittest.TestCase):

    def setUp(self):
        self.ivo = Panda("Ivo", "peter@panda.bg", "Male")
        self.gosho = Panda("Gosho", "go@panda.bg", "Female")

    def test_check_name(self):
        self.assertEqual(self.ivo.name, "Ivo")

    def test_check_mail(self):
        self.assertEqual(self.ivo.email, "peter@panda.bg")

    def test_checkGender(self):
        self.assertEqual(self.ivo.gender, "Male")

    def test_check_gender(self):
        self.assertEqual(self.ivo.isMale(), True)

    def test_check_gender_female(self):
        self.assertEqual(self.ivo.isFemale(), False)

    def test_str(self):
        self.assertEqual(self.ivo.__str__(), "Ivo peter@panda.bg Male")

    def test_compare(self):
        self.assertEqual(self.ivo.isFemale(), False)

    def test_check(self):
        self.assertTrue(self.ivo != self.gosho)

    def test_make_frineds(self):
        make_friends(self.ivo, self.gosho)

if __name__ == '__main__':
    unittest.main()
