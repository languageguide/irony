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

class Stimuli (Base):
    __tablename__ = 'stimuli'
    id = Column(Integer, primary_key = True)
    sentence = Column(String(250), nullable = False)
    gender = Column(String(1), nullable = False) # M-F
    target_word_n = Column(String(20), nullable = False)
    target_word_p = Column(String(20), nullable = False)
    sentence_block = Column(String(5), nullable = False) # PB-T-DISTR
    context = Column(String(1), nullable = False) # P-N

class Trials1 (Base):
    __tablename__ = 'trials_1'
    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    stimuli_id = Column(Integer, ForeignKey('stimuli.id'), nullable = False)
    user_response = Column(String(2), nullable = False)
    user_time = Column(Numeric, nullable = False)

# Create an engine that stores data in the local directory's
db_name = 'irony.db'
os.remove(db_name) if os.path.exists(db_name) else None
engine = create_engine('///'.join(['sqlite:', db_name]))

# Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
Base.metadata.create_all(engine)
