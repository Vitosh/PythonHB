from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


Base = declarative_base()


class bank_clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(Integer)
    balance = Column(Float)
    message = Column(String)
    mail = Column(String)

    def __str__(self):
        return "{} {} {} {} {} {}".format(self.id, self.username, self.password, self.balance, self.message, self.balance)

    def __repr__(self):
        return self.__str__()

engine = create_engine("sqlite:///bank.db")
Base.metadata.create_all(engine)


session = Session(bind=engine)

session.add_all([
    bank_clients(username="Pesho", password="pw1", balance=200.21,
                 message="Hello!1", mail="my@ma.il"),
    bank_clients(username="Gosho", password="pw2", balance=200.22,
                 message="Hello!2", mail="my@ma.il"),
    bank_clients(username="Atanas", password="pw3", balance=200.23,
                 message="Hello!3", mail="my@ma.il"),
    bank_clients(username="Ivan", password="pw4", balance=200.24,
                 message="Hello!4", mail="my@ma.il"),
    bank_clients(username="Drago", password="pw5", balance=200.25,
                 message="Hello!5", mail="my@ma.il")
])

all_clients = session.query(bank_clients.id, bank_clients.username, bank_clients.balance)

for row in all_clients:
    print (row)
