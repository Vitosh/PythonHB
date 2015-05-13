from database_manager import BankDatabaseManager
from getpass import getpass
from client import Client
from mail import send_mail


class CliInterface():

    def __init__(self):
        self.__manager = BankDatabaseManager()
        self.WrongPasswordAttempts = 2

    def command_dispatcher(self, command):
        if command == "register":
            self.register()
        elif command == "login":
            self.login()
        elif command == "info":
            self.info()
        elif command == "exit":
            self.exit_program()
        elif command == "reset":
            self.reset_password()
        else:
            self.not_valid()

    def reset_password(self):
        email = input("Enter your e-mail for password reset:")
        newPassword = Client.generate_random_password()
        hashNewPassword = self.__manager.hash_password(newPassword)
        if (self.__manager.update_hash_password(email, hashNewPassword)):
            # for testing purposes, the only e-mail that may receive mails is my e-mail.
            # You may change it by adding "email" at the end of the send_mail()
            # parameters.
            username = self.__manager.get_username_from_email()
            send_mail(username, hash_password)
            print("Password request has been made.")

    def not_valid(self):
        print("Not a valid command.\nTry again.")

    def exit_program(self):
        print("Thank you for using the bank app!")
        exit()

    def start(self):
        print(
            """Welcome to our bank service. You are not logged in. \n Please register or login""")
        while True:
            command = input("Enter a command:")
            self.command_dispatcher(command)

    def info(self):
        print("login - for logging in!")
        print("register - for creating new account!")
        print("exit - for closing program!")

    def login(self):
        username = input("Enter your username: ")
        password = getpass(prompt="Enter your password: ", stream=None)

        logged_user = self.__manager.login(username, password)

        if logged_user:
            self.logged_menu(logged_user)
            self.WrongPasswordAttempts = 5
        else:
            print("Login failed")
            if (self.WrongPasswordAttempts > 1):
                self.WrongPasswordAttempts -= 1
                print(
                    "You have {} tries left".format(self.WrongPasswordAttempts))
            else:
                print("Are you human or are you robot? :)")
                print("Database is locked for 10 seconds. Enjoy your day!")
                self.__manager.lock_database()

    def register(self):
        username = input("Enter your username: ")
        password = getpass(prompt="Enter your password: ", stream=None)
        mail = input("Enter your mail: ")

        if (self.__manager.register(username, password, mail)):
            print("Registration Successfull")
        else:
            print("Registration failed.")

    def __logged_dispatcher(self, command, logged_user):

        if command == 'info':
            self.logged_info(logged_user)
        elif command == 'changepass':
            self.logged_changepass(logged_user)

        elif command == 'change-message':
            self.logged_change_message(logged_user)

        elif command == 'show-message':
            self.logged_show_message(logged_user)

        elif command == 'help':
            self.logged_help()

        elif command == 'close':
            self.exit_program()
        else:
            self.not_valid()

    def logged_info(self, logged_user):
        print("You are: " + logged_user.get_username())
        print("Your id is: " + str(logged_user.get_id()))
        print(
            "Your balance is:" + str(logged_user.get_balance()) + '$')

    def logged_changepass(self, logged_user):
        new_pass = getpass(prompt="Enter your new password: ", stream=None)
        self.__manager.change_pass(new_pass, logged_user)

    def logged_change_message(self, logged_user):
        new_message = input("Enter your new message: ")
        self.__manager.change_message(new_message, logged_user)

    def logged_show_message(self, logged_user):
        print(logged_user.get_message())

    def logged_help(self):
        print("info - for showing account info")
        print("changepass - for changing passowrd")
        print("change-message - for changing users message")
        print("show-message - for showing users message")

    def logged_menu(self, logged_user):
        print("Welcome you are logged in as: " + logged_user.get_username())

        while True:
            command = input("Logged>>\n Now enter a command:")
            self.__logged_dispatcher(command, logged_user)

a = CliInterface()
a.start()
