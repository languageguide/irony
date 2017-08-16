import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Boolean, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User (Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True, autoincrement = True)
    age = Column(Integer, nullable = False)
    hand = Column(String(1), nullable = False) # D-S
    gender = Column(String(1), nullable = False) # TODO fix ENUM type in sqlalchemy - M-F
    file_name = Column(String(250), nullable = False) # The file name from where the data are taken

class Sentence (Base):
    __tablename__ = 'sentence'
    id = Column(Integer, primary_key = True)
    phrase = Column(String(250), nullable = False)
    gender = Column(String(1), nullable = False) # M-F
    target_word_n = Column(String(20), nullable = False)
    target_word_p = Column(String(20), nullable = False)
    sentence_block = Column(String(5), nullable = False) # PB-T-DISTR
    context = Column(String(1), nullable = False) # P-N

# Create an engine that stores data in the local directory's
file_name = 'irony.db'
os.remove(file_name) if os.path.exists(file_name) else None
engine = create_engine('///'.join(['sqlite:', file_name]))

# Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
Base.metadata.create_all(engine)
