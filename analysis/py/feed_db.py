# Tested with Python 2.7.10
import xlrd, glob, csv, os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Base, User, Stimuli, Trials1, Trials2

class FeedDB:

    def __init__(self, db_name, pathname):
        os.remove(db_name) if os.path.exists(db_name) else None
        engine = create_engine('///'.join(['sqlite:', db_name]))
        Base.metadata.create_all(engine) # Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
        self.file_objects = list(map((lambda file: xlrd.open_workbook(file)), self.__get_files(pathname)))
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
        return glob.glob(pathname)

    def __get_user(self, sheet, user_id):
        age = self.__get_cell_value(sheet, 31, 2)
        hand = self.__get_cell_value(sheet, 34, 2)
        gender = self.__get_cell_value(sheet, 35, 2)
        return User(id = user_id, age = age, hand = hand, gender = gender)

    def __get_stimuli(self, row):
        id = int(row['uid'])
        sentence = row['sentence'].decode('utf-8')
        sentence_block = row['sentenceBlock']
        context = row['context']
        irony_type = row['ironyType']
        gender = row['gender']
        target_word_p = row['targetWordP']
        target_word_n = row['targetWordN']
        # TODO Apply the spread operator - deal with functions having long list of arguments?
        return Stimuli(id = id, sentence = sentence, sentence_block = sentence_block, context = context, gender = gender, target_word_p = target_word_p, target_word_n = target_word_n, irony_type = irony_type)

    def __get_user_response(self, cell_value):
        return 'PA' if cell_value == "'1'" else 'NA'

    def __get_trials1(self, sheet, user_id, nrow):
        stimuli_id = int(self.__get_cell_value(sheet, nrow, 3))
        user_response = self.__get_user_response(self.__get_cell_value(sheet, nrow, 14))
        user_time = self.__get_cell_value(sheet, nrow, 15)
        return Trials1(user_id = user_id, stimuli_id = stimuli_id, user_response = user_response, user_time = user_time)

    def __get_trials2(self, sheet, user_id, nrow):
        stimuli_id = int(self.__get_cell_value(sheet, nrow, 3))
        user_response = self.__get_user_response(self.__get_cell_value(sheet, nrow, 11))
        user_time = self.__get_cell_value(sheet, nrow, 12)
        missing_TW = self.__get_cell_value(sheet, nrow, 1)
        return Trials2(user_id = user_id, stimuli_id = stimuli_id, user_response = user_response, user_time = user_time, missing_TW = missing_TW)

    def __set(self, data):
        self.session.add(data)
        self.session.commit()

    def set_users(self):
        for user_id, file_object in enumerate(self.file_objects):
            self.__set(self.__get_user(file_object.sheet_by_index(0), user_id))

    def set_trials1(self, nrows = 27):
        for user_id, file_object in enumerate(self.file_objects):
            sheet = file_object.sheet_by_index(0)
            for row in xrange(2, nrows + 1):
                self.__set(self.__get_trials1(sheet, user_id, row))

    def set_trials2(self, nrows = 43):
        for user_id, file_object in enumerate(self.file_objects):
            sheet = file_object.sheet_by_index(1)
            for row in xrange(2, nrows + 1):
                self.__set(self.__get_trials2(sheet, user_id, row))

    def set_stumuli(self, pathname):
        with open(pathname, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.__set(self.__get_stimuli(row))

feedDB = FeedDB('irony.db', '../../data/*.xlsx')
feedDB.set_users()
feedDB.set_trials1()
feedDB.set_trials2()
feedDB.set_stumuli('../../stimuli/stories1.csv')
feedDB.set_stumuli('../../stimuli/stories2.csv')
