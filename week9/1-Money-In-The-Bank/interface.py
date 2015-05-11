class CliInterface:

    def __init__(self, bank_manager):
        self.__manager = bank_manager

    def __command_dispatcher(self, command):
        if command == "register":
            self.show_movies()
        elif command == "login":
            pass
        elif command == "help":
            pass
        elif command == "exit":
            pass
        else:
            print("Not a valid command")

    def start(self):
        print(
            """Welcome to our bank service. You are not logged in. \n Please register or login""")
        while True:
            command = input("Enter command:")
            self.__command_dispatcher(command)


# COPIED ==v

    def help(self):
        print("login - for logging in!")
        print("register - for creating new account!")
        print("exit - for closing program!")

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        logged_user = sql_manager.login(username, password)

        if logged_user:
            logged_menu(logged_user)
        else:
            print("Login failed")

    def register(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        sql_manager.register(username, password)

        print("Registration Successfull")

    def logged_menu(self, logged_user):
        print("Welcome you are logged in as: " + logged_user.get_username())
        while True:
            command = input("Logged>>")

            if command == 'info':
                print("You are: " + logged_user.get_username())
                print("Your id is: " + str(logged_user.get_id()))
                print(
                    "Your balance is:" + str(logged_user.get_balance()) + '$')

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
