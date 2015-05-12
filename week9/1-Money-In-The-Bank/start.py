import sqlite3
from settings import DB_NAME
from database_manager import BankDatabaseManager
from interface import CliInterface


def main():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    bank_manager = BankDatabaseManager(conn)
    interface = CliInterface(bank_manager)

    interface.start()

if __name__ == "__main__":
    main()
