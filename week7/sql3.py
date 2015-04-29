import sqlite3

connection = sqlite3.connect("users2.db")
cursor = connection.cursor()

# create_users_table = """
# CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, monthly_salary INTEGER, yearly_bonus INTEGER, position TEXT)
# """

# update_users_table = """
# INSERT
# INTO users (name, monthly_salary,yearly_bonus,position)
# VALUES
# ("Ivan Ivanov", 5000, 10000, "SD"),
# ("Rado Rado", 500, 0, "Intern"),
# ("Ivo Ivo", 10000, 10000, "CEO"),
# ("Petar Petrov", 5000, 10000, "Marketing Manager"),
# ("Maria Georgieva", 5000, 10000, "COO");
# """

# cursor.execute(create_users_table)
# cursor.execute(update_users_table)


def le():
    sqlText = "SELECT id,name,position FROM users"
    cursor.execute(sqlText)
    rows = cursor.fetchall()
    for r in rows:
        print(r)


def ms():
    sqlText = "SELECT sum(monthly_salary) FROM users"
    cursor.execute(sqlText)
    result = cursor.fetchall()[0][0]
    print("The company is spending {} monthly.".format(result))


def ys():
    sqlText1 = "SELECT sum(monthly_salary) FROM users"
    sqlText2 = "SELECT sum(yearly_bonus) FROM users"
    cursor.execute(sqlText1)
    result = cursor.fetchall()[0][0]
    result = 12 * result
    cursor.execute(sqlText2)
    bonus = cursor.fetchall()[0][0]
    print("Total annual salaries are {}.".format(result))
    print("Total annual bonuses are {}.".format(bonus))
    print("Total annual spending {}.".format(result + bonus))


def ae():
    input_Name = input("Name:")
    input_Salary = input("Salary:")
    input_Bonus = input("Bonus:")
    input_Position = input("Position:")

    sqlText = """INSERT INTO users (name, monthly_salary,yearly_bonus,position) 
    VALUES({},{},{},{})""".format(input_Name, input_Salary, input_Bonus, input_Position)

    cursor.execute(sqlText)
    le()

input_var = input("Enter a command:")
eval(input_var)
