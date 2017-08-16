# Tested with Python 2.7.10
import xlrd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import User, Base

# TODO from functional to OOP

def get_cell_value(sheet, row, col):
    return sheet.cell_value(rowx = row - 1, colx = col - 1)

def get_file_object(file):
    print file
    file_object = xlrd.open_workbook(file)

    print "The number of worksheets is", file_object.nsheets
    print "Worksheet name(s):", file_object.sheet_names()
    sheet1 = file_object.sheet_by_index(0)
    print sheet1.name, sheet1.nrows, sheet1.ncols
    age = get_cell_value(sheet1, 31, 2)
    hand = get_cell_value(sheet1, 34, 2)
    gender = get_cell_value(sheet1, 35, 2)
    print 'age: ', age, 'hand: ', hand,'gender: ', gender


    # Insert a user in the user table
    new_user = User(age = age, hand = hand, gender = gender, file_name = file)
    session.add(new_user)
    session.commit()

def get_files():
    # It returns a list with the data xlsx files
    import glob
    return glob.glob("../data/*.xlsx")


# TODO - the sqlite file should be taken from a configuration file
engine = create_engine('sqlite:///irony.db')
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
session = DBSession()

files = get_files()[0:3]
for file in files:
    get_file_object(file)

