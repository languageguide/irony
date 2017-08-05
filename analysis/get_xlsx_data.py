# Tested with Python 2.7.10
import xlrd

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

def get_files():
    # It returns a list with the data xlsx files
    import glob
    return glob.glob("../data/*.xlsx")

files = get_files()[0:1]
for file in files:
    get_file_object(file)

