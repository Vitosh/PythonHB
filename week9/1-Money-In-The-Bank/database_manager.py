import sqlite3
from settings import DB_NAME
from Client import Client

class BankDatabaseManager:

    def __init__(self, conn):
        self.__conn = conn

    def change_message(self, new_message, logged_user):
        cursor = self.__conn.cursor()

        update_sql = "UPDATE clients SET message = ? WHERE id = ?"
        cursor.execute(update_sql, (new_message, logged_user.get_id()))
        self.__conn.commit()
        logged_user.set_message(new_message)

    def change_pass(self, new_pass, logged_user):
        cursor = self.__conn.cursor()

        update_sql = "UPDATE clients SET password = ? WHERE id = ?"
        cursor.execute(update_sql, (new_pass, logged_user.get_id()))
        self.__conn.commit()

    def register(self, username, password):
        cursor = self.__conn.cursor()
        insert_sql = "insert into clients (username, password) values (?, ?)"
        cursor.execute(insert_sql, (username, password))
        self.__conn.commit()

    def login(self, username, password):
        cursor = self.__conn.cursor()
        select_query = "SELECT id, username, balance, message FROM clients WHERE username = ? AND password = ? LIMIT 1"

        cursor.execute(select_query, (username, password))
        user = cursor.fetchone()

        if(user):
            return Client(user[0], user[1], user[2], user[3])
        else:
            return False
