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
    context = Column(String(1), nullable = False) # P(positive context) N(negative context)
    irony_type = Column(String(1), nullable = False) # I(ironic) S(sarcastic)

class Trials1 (Base):
    __tablename__ = 'trials_1'
    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    stimuli_id = Column(Integer, ForeignKey('stimuli.id'), nullable = False)
    user_response = Column(String(2), nullable = False) # PA(positive adjective) NA (negative adjective)
    user_time = Column(Numeric, nullable = False)

class Trials2 (Base):
    __tablename__ = 'trials_2'
    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    stimuli_id = Column(Integer, ForeignKey('stimuli.id'), nullable = False)
    user_response = Column(String(2), nullable = False) 
    user_time = Column(Numeric, nullable = False)
    missing_TW = Column(String(20), nullable = False)
