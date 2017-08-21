# Tested with Python 2.7.10
import xlrd, glob
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import User, Stimuli, Base

class FeedDB:

    def __init__(self, db_name):
        self.db_name = db_name
        self.__set_session()

    def __set_session(self):
        # TODO - the sqlite file should be taken from a configuration file since it appears in create_db.py, too.
        engine = create_engine('///'.join(['sqlite:', self.db_name]))
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def __get_cell_value(self, sheet, row, col):
        return sheet.cell_value(rowx = row - 1, colx = col - 1)

    def __get_files(self, pathname):
        # It returns a list with the data xlsx files
        return glob.glob(pathname)[0:5]

    def __get_user(self, sheet):
        age = self.__get_cell_value(sheet, 31, 2)
        hand = self.__get_cell_value(sheet, 34, 2)
        gender = self.__get_cell_value(sheet, 35, 2)
        return User(age = age, hand = hand, gender = gender)

    def __get_stimuli(self, row):
        id = int(row['uid'])
        sentence = row['sentence']
        sentence_block = row['sentenceBlock']
        context = row['context']
        gender = row['gender']
        target_word_p = row['targetWordP']
        target_word_n = row['targetWordN']
        # TODO Apply the spread operator
        return Stimuli(id = id, sentence = sentence, sentence_block = sentence_block, context = context, gender = gender, target_word_p = target_word_p, target_word_n = target_word_n)

    def __set(self, data):
        self.session.add(data)
        self.session.commit()

    def set_users(self, pathname):
        file_objects = list(map((lambda file: xlrd.open_workbook(file)), self.__get_files(pathname)))
        for file_object in file_objects:
            self.__set(self.__get_user(file_object.sheet_by_index(0)))

    def set_stumuli(self, pathname):
        import csv
        with open(pathname, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.__set(self.__get_stimuli(row))

feedDB = FeedDB('irony.db')
feedDB.set_users('../data/*.xlsx')
feedDB.set_stumuli('../stimuli/stories1.csv')
feedDB.set_stumuli('../stimuli/stories2.csv')
