"""
    SQLAlchemy models to user table
"""
import os

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import desc
from passlib.context import CryptContext


from .server import create_engine_data

engine = create_engine_data()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    username = Column(String(30), primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(100), unique=True)
    password = Column(String(250))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student = Column(String(10), ForeignKey("students.identification"))
    is_aprove  = Column(String(2), default='0')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    students = relationship("Student", back_populates="requests")


class Student(Base):
    __tablename__ = "students"

    identification = Column(String(10), primary_key=True)
    name = Column(String(30))
    lastname = Column(String(30))
    age = Column(Integer)
    email = Column(String(100), unique=True)
    grimoire = Column(Integer, ForeignKey("grimoires.id"))
    affinity = Column(Integer, ForeignKey("magicaffinities.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    affinities = relationship("MagicAffinity", back_populates="students")
    grimoires = relationship("Grimoire", back_populates="students")
    requests = relationship(
        "Request",
        back_populates="students",
        order_by=desc(Request.created_at))


class MagicAffinity(Base):
    __tablename__ = "magicaffinities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), unique=True)

    students = relationship("Student", back_populates="affinities")


class Grimoire(Base):
    __tablename__ = "grimoires"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), unique=True)

    students = relationship("Student", back_populates="grimoires")


def insert_initial_data():
    try:
        session = Session(bind=engine)
        session.add_all([
            Grimoire(name='Sinceridad'),
            Grimoire(name='Esperanza'),
            Grimoire(name='Amor'),
            Grimoire(name='Buena Fortuna'),
            Grimoire(name='Desesperación'),
            MagicAffinity(name='Oscuridad'),
            MagicAffinity(name='Luz'),
            MagicAffinity(name='Fuego'),
            MagicAffinity(name='Agua'),
            MagicAffinity(name='Viento'),
            MagicAffinity(name='Tierra'),
            User(
                username='test',
                first_name="test 1",
                last_name="test 1",
                email="test@test.com",
                password=pwd_context.hash("password123."))
        ])
        session.commit()
    except IntegrityError as _:
        print("Data was save!")

def create_table():
    """Create the tables on teh Data Base
    """
    Base.metadata.create_all(
        engine,
        checkfirst=True)
    insert_initial_data()
