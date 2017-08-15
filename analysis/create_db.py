import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Boolean, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Person (Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    id = Column(Integer, primary_key = True)
    age = Column(Integer, nullable = False)
    hand = Column(String(1), nullable = False)
    # TODO fix enum type in sqlalchemy
    gender = Column(Enum('M', 'F'), nullable = False)
    # The file name from where the data are taken
    file_name = Column(String(250), nullable = False)

class Sentence (Base):
    __tablename__ = 'sentence'
    # Here we define columns for the table person
    id = Column(Integer, primary_key = True)
    phrase = Column(String(250), nullable = False)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///irony.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
