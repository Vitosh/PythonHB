import unittest
import os
import create_db
from database_manager import BankDatabaseManager
from settings import DB_NAME


class SqlManagerTests(unittest.TestCase):

    def setUp(self):
        create_db.generate_tables()
        self.newDB = BankDatabaseManager()
        self.newDB.register("Tester", "123BatMAN!1", "jobanana75@yahoo.com")

    def tearDown(self):
        self.newDB.cursor.execute('DROP TABLE clients')

    @classmethod
    def tearDownClass(cls):
        os.remove(DB_NAME)

    def test_mail(self):
        self.newDB.cursor.execute(
            """SELECT mail
            FROM clients
            where username = (?);
            """, ("Tester", )
        )
        user_result = self.newDB.cursor.fetchone()
        self.assertEqual(user_result[0], "jobanana75@yahoo.com")

        # self.newDB.

    def test_register(self):
        password = "123123BatMAN!1"
        self.newDB.register("Dinko", password, "jobanana75@yahoo.com")
        password = self.newDB.hash_password(password)

        self.newDB.cursor.execute(
            """SELECT Count(*)
               FROM clients
               WHERE username = (?)
               AND password = (?)""", ('Dinko', password))
        users_count = self.newDB.cursor.fetchone()
        self.assertEqual(users_count[0], 1)

    def test_name(self):
        self.newDB.register(
            'Peter', 'harrypotteralealeBatMAN!1', "jobanana75@yahoo.com")
        self.newDB.cursor.execute(
            """SELECT username, password, balance, message
               FROM clients""")
        user_info = self.newDB.cursor.fetchall()
        self.assertEqual(user_info[1][0], "Peter")
        self.assertEqual(user_info[0][0], "Tester")

    def test_login(self):
        logged_user = self.newDB.login('Tester', '123BatMAN!1')
        self.assertEqual(logged_user.get_username(), 'Tester')

    def test_login_wrong_password(self):
        logged_user = self.newDB.login('Tester', '123567BatMAN!1')
        self.assertFalse(logged_user)

    def test_change_message(self):
        logged_user = self.newDB.login(
            "Tester", "123BatMAN!1")
        new_message = "podaivinototam"
        self.newDB.change_message(new_message, logged_user)
        self.assertEqual(logged_user.get_message(), new_message)

    def test_change_password(self):
        logged_user = self.newDB.login('Tester', '123BatMAN!1')
        new_password = "12345BatMAN!1"
        # new_password = self.newDB.hash_password(new_password)
        self.newDB.change_pass(new_password, logged_user)

        logged_user_new_password = self.newDB.login('Tester', new_password)
        self.assertEqual(logged_user_new_password.get_username(), 'Tester')

    def test_check_password_stability_1(self):
        self.assertFalse(
            self.newDB.check_password("Vitomir1!2", username="Vitomir"))

    def test_check_password_stability_2(self):
        self.assertFalse(
            self.newDB.check_password("vitomir12", username="Vitmir"))

    def test_check_password_stability_3(self):
        self.assertTrue(
            self.newDB.check_password("VitoshASDmy!com@1123", username="BomirPetrov"))

    def test_check_password_stability_4(self):
        self.assertFalse(
            self.newDB.check_password("Vitoshacademy!com!1", username="Vitosh"))

    def test_check_password_stability_5(self):
        self.assertFalse(
            self.newDB.check_password("@DFfdgfdgfds", username="Vitosh"))

    def test_check_password_stability_6(self):
        self.assertTrue(
            self.newDB.check_password("@DFfdgfdgfds123", username="Vitosh"))

    def test_check_password_stability_7(self):
        self.assertFalse(
            self.newDB.check_password("DFfdgfdgfds123123123", username="Vitosh"))


if __name__ == '__main__':
    unittest.main()
