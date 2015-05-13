import random
import string


class Client():

    def __init__(self, id, username, balance, message, mail):
        self.__username = username
        self.__balance = balance
        self.__id = id
        self.__message = message
        self.__mail = mail

    def get_mail(self):
        return self.__mail

    def get_username(self):
        return self.__username

    def get_balance(self):
        return self.__balance

    def get_id(self):
        return self.__id

    def get_message(self):
        return self.__message

    def set_message(self, new_message):
        self.__message = new_message

    @staticmethod
    def generate_random_password():
        size = random.randrange(9, 15)
        chars = string.ascii_uppercase + string.digits + \
            string.ascii_lowercase + "!@#$%^&*()"
        return ''.join(random.choice(chars) for _ in range(size))


# test = Client.generate_random_password()
# print(test)
