from settings import DB_SQL_FILE, DB_NAME
import sqlite3


def generate_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    with open(DB_SQL_FILE, "r") as f:
        cursor.executescript(f.read())
