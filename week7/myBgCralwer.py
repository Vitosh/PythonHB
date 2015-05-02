import sqlite3

connection = sqlite3.connect("servers.db")
cursor = connection.cursor()
connection.row_factory = sqlite3.Row


def generate_table():
    create_users_table = """CREATE TABLE IF NOT EXISTS
                        users(id INTEGER PRIMARY KEY, name TEXT, monthly_salary INTEGER, yearly_bonus INTEGER, position TEXT)
                        """
    cursor.execute(create_users_table)


def generate_data():
    update_users_table = """INSERT INTO users (name, monthly_salary,yearly_bonus,position)
                            VALUES
                            ("Ivan Ivanov", 5000, 10000, "SD"),
                            ("Rado Rado", 500, 0, "Intern"),
                            ("Ivo Ivo", 10000, 10000, "CEO"),
                            ("Petar Petrov", 5000, 10000, "Marketing Manager"),
                            ("Maria Georgieva", 5000, 10000, "COO");"""

    cursor.execute(update_users_table)


def list_employees():
    sqlText = """SELECT id,name,position
                 FROM users;"""

    cursor.execute(sqlText)
    rows = cursor.fetchall()
    for r in rows:
        print(r)


def monthly_spending():
    sqlText = """SELECT sum(monthly_salary)
                 FROM users;"""

    cursor.execute(sqlText)
    result = cursor.fetchone()
    print("The company is spending {} every month!".format(result[0]))


def yearly_spending():
    sqlText1 = """SELECT sum(monthly_salary)
                  FROM users;"""

    sqlText2 = """SELECT sum(yearly_bonus)
                  FROM users;"""

    cursor_result = cursor.execute(sqlText1)
    row = cursor_result.fetchone()
    annualSalaries = int(row[0]) * 12

    cursor_result = cursor.execute(sqlText2)
    row = cursor_result.fetchone()
    bonus = int(row[0])

    print("Total annual salaries are {}.".format(annualSalaries))
    print("Total annual bonuses are {}.".format(bonus))
    print("Total annual spending {}.".format(annualSalaries + bonus))


def add_employee():
    input_Name = str(input("Name:"))
    input_Salary = int(input("Salary:"))
    input_Bonus = int(input("Bonus:"))
    input_Position = str(input("Position:"))

    sqlText = """INSERT INTO users (name, monthly_salary,yearly_bonus,position)
                 VALUES(?,?,?,?);"""

    cursor.execute(sqlText,
                   (input_Name, input_Salary, input_Bonus, input_Position))
    list_employees()


def delete_employee():
    input_id = int(input("ID for deletion:"))
    sqlText = """DELETE FROM users
                 WHERE id = ?;"""

    cursor.execute(sqlText, (input_id,))
    list_employees()


def update_employee():
    input_id = int(input("ID for update:"))
    input_Name = str(input("Name:"))
    input_Salary = int(input("Salary:"))
    input_Bonus = int(input("Bonus:"))
    input_Position = str(input("Position:"))

    sqlText = """UPDATE users
                 SET name = ?, monthly_salary = ?, yearly_bonus = ?, position = ?
                 WHERE id = ?;"""

    cursor.execute(sqlText,
                   (input_Name, input_Salary, input_Bonus, input_Position, input_id))
    list_employees()


input_var = input("Enter a command:")
eval(input_var + "()")

connection.commit()
cursor.close()
connection.close()
