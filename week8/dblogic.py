import sqlite3
import hr


VAR_DB_NAME = "studentsData.db"


def create_tables():

    con = sqlite3.connect(VAR_DB_NAME)
    cur = con.cursor()

    createTableCourses = """CREATE TABLE IF NOT EXISTS Courses(
                            course_id INTEGER PRIMARY KEY,
                            course_title TEXT);"""

    createTableStudents = """CREATE TABLE IF NOT EXISTS Students(
                            student_id INTEGER PRIMARY KEY,
                            student_name TEXT,
                            student_github TEXT,
                            student_course INTEGER,
                            FOREIGN KEY(student_course) REFERENCES Courses(course_id));"""

    createTableMatch = """CREATE TABLE IF NOT EXISTS Match(
                            match_id INTEGER PRIMARY KEY,
                            match_student_id INTEGER,
                            match_course_id INTEGER,
                            FOREIGN KEY (match_student_id) REFERENCES Students(student_id),
                            FOREIGN KEY (match_course_id) REFERENCES Courses(course_id)
                            );"""

    for sqlQuery in [createTableCourses, createTableStudents, createTableMatch]:
        cur.execute(sqlQuery)

    con.commit()
    cur.close()
    con.close()


def fill_tables(allCourses, allStudents):

    con = sqlite3.connect(VAR_DB_NAME)
    cur = con.cursor()

    sqlCourses = ""
    sqlStudent = ""

    for course in allCourses:
        sqlCourses = sqlCourses + "(\"" + course + "\"),"

    sqlCourses = sqlCourses[:-1]

    fillTableCourses = """INSERT INTO Courses (course_title)
                       VALUES {};""".format(sqlCourses)

    # for student in allStudents:
    #     sqlStudent = sqlStudent + "(\"" + student + "\",\"" + allStudents[student] + "\"),"

    sqlStudent = sqlStudent[:-1]
    cur.execute(fillTableCourses)

    # Maximum 500 rows per once, so I am doing it line by line here:
    for student in allStudents:
        fillTableStudents = """INSERT INTO Students(student_name, student_github, student_course)
                            VALUES (?,?,?);"""
        valueName = student[0]
        valueGit = student[1]
        valueCourse = student[2]

        cur.execute(fillTableStudents, (valueName, valueGit, valueCourse))

    con.commit()
    cur.close()
    con.close()


def delete_tables():
    con = sqlite3.connect(VAR_DB_NAME)
    cur = con.cursor()

    delete_courses = """DELETE FROM Courses;"""
    delete_students = """DELETE FROM Students;"""
    delete_match = """DELETE FROM Match;"""

    for sqlQuery in [delete_courses, delete_students, delete_match]:
        cur.execute(sqlQuery)

    con.commit()
    cur.close()
    con.close()


def t1():
    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row

    sqlTask = "SELECT student_name, student_github FROM Students;"

    cursor.execute(sqlTask)
    rows = cursor.fetchall()
    for r in rows:
        print(r)

    connection.commit()
    cursor.close()
    connection.close()


def t2():
    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row

    sqlTask = "SELECT course_title FROM Courses;"

    cursor.execute(sqlTask)
    rows = cursor.fetchall()
    for r in rows:
        print(r)

    connection.commit()
    cursor.close()
    connection.close()


def t3():
    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row

    sqlTask = "SELECT student_name, student_course FROM Students;"

    cursor.execute(sqlTask)
    rows = cursor.fetchall()
    for r in rows:
        print(r)

    connection.commit()
    cursor.close()
    connection.close()


def t4():
    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row

    sqlTask = """SELECT student_name, student_course, COUNT(student_name) 
                FROM Students
                GROUP BY student_name
                ORDER BY COUNT(student_name) DESC
                LIMIT 10;"""

    cursor.execute(sqlTask)
    rows = cursor.fetchall()
    for r in rows:
        print(r)

    connection.commit()
    cursor.close()
    connection.close()


create_tables()
fill_tables(hr.get_all_courses(), hr.generate_data_student_table())

input_var = input("Enter a command:")
eval(input_var + "()")
