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


import sql_manager


def main_menu():
    print(
        "Welcome to our bank service. You are not logged in. \nPlease register or login")

    while True:
        command = input("$$$>")

        if command == 'register':
            register()
        elif command == 'login':
            login()
        elif command == 'help':
            help()
        elif command == 'exit':
            break
        else:
            print("Not a valid command")


def help():
    print("login - for logging in!")
    print("register - for creating new account!")
    print("exit - for closing program!")


def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    logged_user = sql_manager.login(username, password)

    if logged_user:
        logged_menu(logged_user)
    else:
        print("Login failed")


def register():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    sql_manager.register(username, password)

    print("Registration Successfull")


def logged_menu(logged_user):
    print("Welcome you are logged in as: " + logged_user.get_username())
    while True:
        command = input("Logged>>")

        if command == 'info':
            print("You are: " + logged_user.get_username())
            print("Your id is: " + str(logged_user.get_id()))
            print("Your balance is:" + str(logged_user.get_balance()) + '$')

        elif command == 'changepass':
            new_pass = input("Enter your new password: ")
            sql_manager.change_pass(new_pass, logged_user)

        elif command == 'change-message':
            new_message = input("Enter your new message: ")
            sql_manager.change_message(new_message, logged_user)

        elif command == 'show-message':
            print(logged_user.get_message())

        elif command == 'help':
            print("info - for showing account info")
            print("changepass - for changing passowrd")
            print("change-message - for changing users message")
            print("show-message - for showing users message")


def main():
    sql_manager.create_clients_table()
    main_menu()

if __name__ == '__main__':
    main()
