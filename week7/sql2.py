import sqlite3

connection = sqlite3.connect("users.db")
cursor = connection.cursor()

create_users_table = """
CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, email TEXT, gender TEXT)
"""
cursor.execute(create_users_table)
connection.commit()


# ~/Desktop/101/week7sqlite3 users.db
# SQLite version 3.8.2 2013-12-06 14:53:30
# Enter ".help" for instructions
# Enter SQL statements terminated with a ";"
# sqlite> .tables
# users
# sqlite> .schema users
