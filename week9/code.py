from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship


Base = declarative_base()


class bank_clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(Integer)
    balance = Column(Float)
    message = Column(String)
    mail = Column(String)

engine = create_engine("sqlite:///bank.db")
Base.metadata.create_all(engine)

# Session is our Data Mapper
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


# SELECT * FROM student WHERE name = "Rado" LIMIT 2;
rado = session.query(Student).filter(Student.name == "Rado").one()

# Now, lets add some grades to rado:

rado.grades = [Grade(value=6), Grade(value=5), Grade(value=3)]
session.commit()

# And add grades to ivo

ivo = session.query(Student).filter(Student.name == "Ivo").one()
ivo.grades.append(Grade(value=6))
