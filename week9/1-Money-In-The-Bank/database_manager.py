from Client import Client
import sqlite3
import create_db
from settings import DB_NAME
import hashlib
import time


class BankDatabaseManager():

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        create_db.generate_tables()

    def change_message(self, new_message, logged_user):

        update_sql = "UPDATE clients SET message = ? WHERE id = ?"
        self.cursor.execute(update_sql, (new_message, logged_user.get_id()))
        self.conn.commit()
        logged_user.set_message(new_message)

    def change_pass(self, new_pass, logged_user):
        if not BankDatabaseManager.check_password(new_pass, logged_user=logged_user):
            return
        cursor = self.conn.cursor()
        new_pass = BankDatabaseManager.hash_password(new_pass)
        update_sql = "UPDATE clients SET password = ? WHERE id = ?"
        cursor.execute(update_sql, (new_pass, logged_user.get_id()))
        self.conn.commit()

    def register(self, username, password):
        if not BankDatabaseManager.check_password(password, username=username):
            return False

        HashedPassword = BankDatabaseManager.hash_password(password)

        cursor = self.conn.cursor()
        insert_sql = "insert into clients (username, password) values (?, ?)"
        cursor.execute(insert_sql, (username, HashedPassword))
        self.conn.commit()
        return True

    def login(self, username, password):
        cursor = self.conn.cursor()
        HashedPassword = BankDatabaseManager.hash_password(password)

        select_query = "SELECT id, username, balance, message FROM clients WHERE username = ? AND password = ? LIMIT 1"

        cursor.execute(select_query, (username, HashedPassword))
        user = cursor.fetchone()

        if(user):
            return Client(user[0], user[1], user[2], user[3])
        else:
            return False

    @staticmethod
    def check_password(password, username="", logged_user=""):
        sPasswordInUserName = "Your password should not be part of your user name!"
        sPasswordTooShort = "Your current password is only {} symbols\n It should be above 8."
        sPasswordNotVarious = "Your password should have capital letters, number and special symbol"

        if len(password) < 9:
            print(sPasswordTooShort.format(len(password)))
            return False
        if username != "":
            if username.lower() in password.lower():
                return False
        else:
            if logged_user.get_username().lower() in password.lower():
                print(sPasswordInUserName)
                return False
        # Checking for capital letter, digit, lower letter and special char.
        if not(bool([char for char in password if (char.isupper())]) and bool([char for char in password if (char.isdigit())]) and bool([char for char in password if (char.islower())]) and bool(set('[~!@#$%^&*()_+.{}":;\']+$').intersection(password))):
            print(sPasswordNotVarious)
            return False

        return True

    @staticmethod
    def hash_password(password):
        pwd = hashlib.md5(password.encode())
        return pwd.hexdigest()

    @staticmethod
    def lock_database():

        z = 10
        while z > 0:
            time.sleep(1)
            print("{} minutes to unlocking!".format(z))
            z -= 1
        print("Database is now unlocked! Good luck!")
