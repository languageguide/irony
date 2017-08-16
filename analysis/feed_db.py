# Tested with Python 2.7.10
import xlrd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import User, Base

class FeedDB:

    def __init__(self, db_name):
        # TODO - the sqlite file should be taken from a configuration file
        engine = create_engine('///'.join(['sqlite:', db_name]))
        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        self.session = DBSession()
        self.pathname = '../data/*.xlsx'

        files = self.get_files()[0:3]
        for file in files:
            self.get_file_object(file)

    def get_cell_value(self, sheet, row, col):
        return sheet.cell_value(rowx = row - 1, colx = col - 1)

    def get_file_object(self, file):
        file_object = xlrd.open_workbook(file)
        print "The number of worksheets is", file_object.nsheets
        print "Worksheet name(s):", file_object.sheet_names()
        self.set(self.get_user(file_object.sheet_by_index(0), file))

    def get_files(self):
        # It returns a list with the data xlsx files
        import glob
        return glob.glob(self.pathname)

    def get_user(self, sheet, file):
        age = self.get_cell_value(sheet, 31, 2)
        hand = self.get_cell_value(sheet, 34, 2)
        gender = self.get_cell_value(sheet, 35, 2)
        print age
        # Insert a user in the user table
        return User(age = age, hand = hand, gender = gender, file_name = file)

    def set(self, data):
        self.session.add(data)
        self.session.commit()


feedDB = FeedDB('irony.db')
