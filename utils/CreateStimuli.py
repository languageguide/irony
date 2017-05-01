#!/usr/local/bin/python
# coding: latin-1

"""
Create the story for the second part of the experiment.

The idea of this piece of code is to create a cvs file (data/stories2.cvs) starting from two files:
1. A list of new stories
2. A list of stories taken from the previous experiment and based on the user responses.

"""

import codecs, os, random, csv

class CreateStimuli:

    def __init__(self):

        input_file = './stimuli/stories1.csv'
        output_files = ['./data/stories1.out.csv', './data/stories2.out.csv']
        self.response1_file = 'data/responses1.out'

        self.uui_check = -1
        if os.path.isfile(self.response1_file):
            os.remove(self.response1_file)

        self._listOfList = self._getListOfList(input_file)


        self._writeFile(self._writePB(), output_files[0], 'w')
        self._writeFile(self._writePB(), output_files[1], 'w')
        self._writeFile(self._listOfList, output_files[0], 'a')

    # it create a list of list from a cvs file
    def _getListOfList(self, file_name):
        # TODO: you should write less line of code: http://stackoverflow.com/questions/5518435/python-fastest-way-to-create-a-list-of-n-lists
        rows = []
        list_of_list = []

        f = codecs.open(os.path.realpath(file_name), encoding='utf-8')
        lines = f.readlines()
        self._arguments_header = lines.pop(0) # the first rows are just the header and it will be removed
        rows = rows + lines
        random.shuffle(rows)
        for row in rows:
            list_of_list.append(row.split(","))
        return list_of_list

    def _writePB(self):
        pbs = []
        contexts = ['N', 'P']
        random.shuffle(contexts)
        for context in contexts:
            for list in self._listOfList:
                if (list[1] == "PB" and list[3] == context):
                    self._listOfList.remove(list)
                    pbs.append(list)
                    break
        return pbs

    def _writeFile(self, listOfList, file_name, mode):
        ouptup_file = codecs.open(file_name, mode=mode, encoding='utf-8')
        if mode == 'w':
            ouptup_file.write(self._arguments_header)
        try:
            for list in listOfList:
                ouptup_file.write(','.join(list))
        finally:
            ouptup_file.close()

    def createStoriesFromResponse(self, storiesFile='data/2.out'):
        f = open(self.response1_file, 'r')
        lines = f.readlines()
        for row in lines:
            print row.split(',')

    def record_answer(self, uid, key_resp_1):
        ouptup_file = open(self.response1_file, 'a')
        if self.uui_check == uid :
            return;
        else:
            self.uui_check = uid
        try:
            _string = str(uid) + ',' + str(key_resp_1) + '\n'
            ouptup_file.write(_string)
        finally:
            ouptup_file.close()

    def open_instructions(self, filename):
        return codecs.open(os.path.realpath(filename), encoding='utf-8')





