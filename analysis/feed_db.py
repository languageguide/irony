# Tested with Python 2.7.10
import xlrd, glob
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import User, Base

class FeedDB:

    def __init__(self, pathname, db_name):
        self.db_name = db_name
        self.pathname = pathname
        self.set_session()
        self.file_objects = list(map((lambda file: xlrd.open_workbook(file)), self.get_files()))
        self.set_users()

    def set_session(self):
        # TODO - the sqlite file should be taken from a configuration file since it appears in create_db.py, too.
        engine = create_engine('///'.join(['sqlite:', self.db_name]))
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def get_cell_value(self, sheet, row, col):
        return sheet.cell_value(rowx = row - 1, colx = col - 1)

    def get_files(self):
        # It returns a list with the data xlsx files
        return glob.glob(self.pathname)[0:5]

    def get_user(self, sheet):
        age = self.get_cell_value(sheet, 31, 2)
        hand = self.get_cell_value(sheet, 34, 2)
        gender = self.get_cell_value(sheet, 35, 2)
        return User(age = age, hand = hand, gender = gender)

    def set(self, data):
        self.session.add(data)
        self.session.commit()

    def set_users(self):
        for file_object in self.file_objects:
            self.set(self.get_user(file_object.sheet_by_index(0)))

feedDB = FeedDB('../data/*.xlsx', 'irony.db')
