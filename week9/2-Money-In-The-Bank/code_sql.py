import sqlite3


class bank_clients():

    def __init__(self):
        self.conn = sqlite3.connect("bank.db")
        self.cursor = self.conn.cursor()

    def generate_tables(self):

        sqlCreate = """CREATE TABLE clients(
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        password TEXT,
                        balance REAL,
                        message TEXT,
                        mail TEXT)"""

        self.cursor.execute(sqlCreate)
        self.conn.commit()

    def insert_into_table(self, id, username, password, balance, message, mail):
        sqlInsert = "INSERT into clients (id, username, password, balance, message, mail) values (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(
            sqlInsert, (id, username, password, balance, message, mail))
        self.conn.commit()

    def show(self):
        sqlSelect = "SELECT * FROM clients"
        self.cursor.execute(sqlSelect)
        result = self.cursor.fetchall()

        for row in result:
            print(row)
        # print(result)[0]
        # print(result)[1]

viBank = bank_clients()
viBank.generate_tables()

viBank.insert_into_table(1, "Ivan", "pw1", "300", "I am Ivan", "@v.an")
viBank.insert_into_table(
    2, "Stoyan", "pw2", "312300.12", "I am not Ivan", "i@v.an")
viBank.insert_into_table(
    3, "Kristian", "pw3", "300312.12", "I am not Ivan", "i@v.an")
viBank.insert_into_table(
    4, "Dincho", "pw4", "300123.22", "I am not Ivan", "i@v.an")
viBank.insert_into_table(5, "Mincho", "pw5", "300.12", "I am Mincho", "i@v.an")
viBank.show()
