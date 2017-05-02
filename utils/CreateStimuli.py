#!/usr/local/bin/python
# coding: latin-1

"""
Create the story for the second part of the experiment.

The idea of this piece of code is to create a cvs file (data/stories2.cvs) starting from two files:
1. A list of new stories
2. A list of stories taken from the previous experiment and based on the user responses.

"""

import codecs, os, random, csv, re

class CreateStimuli:

    def __init__(self):

        self.MAX_GOOD_STORIES = 8
        self.FS = ',' # file fields separator
        self.inputFiles = ['./stimuli/stories1.csv', './stimuli/stories2.csv']
        self.outputFiles = ['./data/stories1.out.csv', './data/stories2.out.csv', './data/response.out']
        self.uui_check = -1

        self._removeFiles(self.outputFiles)
        self._listOfList = self._getListOfList()
        self._writeFile(self._getPB(), self.outputFiles[0])
        self._writeFile(self._getPB(storyNum = 2), self.outputFiles[1])
        self._writeFile(self._listOfList, self.outputFiles[0])

    def setStoriesFromResponse(self):

        goodStories = self.getStoriesFromResponse()
        rows1 = self._getLines(self.inputFiles[0])
        allStories = self._getLines(self.inputFiles[0])
        distractors = self._doubleStories(self._getLines(self.inputFiles[1])[1:])
        random.shuffle(distractors)
        allStories = []

        cntDs = 0 # counter distractors
        cntGS = 0 # counter good stories

        for distractor in distractors:
            cntDs += 1
            allStories.append(distractor)
            if cntDs % 4 == 0:
                goodStory = goodStories[cntGS]

                row1Ls = rows1[self._getInt(goodStory)].split(self.FS)
                row1Ls[5] = row1Ls[8 - self._getRsp(goodStory)].rstrip("\n\r") # mark (user response from the first experiment)
                allStories.append(row1Ls)
                cntGS += 1
                if cntGS >= len(goodStories):
                    break

        self._writeFile(allStories, self.outputFiles[1])

    # used from psychoPy
    def getInstructions(self, fileName):
        return self._openFile('/'.join(['instructions', fileName])).read()

    # it create a list of list from a cvs file
    def _getListOfList(self):
        # TODO: you should write less line of code: http://stackoverflow.com/questions/5518435/python-fastest-way-to-create-a-list-of-n-lists
        rows = []
        list_of_list = []
        lines = self._getLines(self.inputFiles[0])
        self._arguments_header = lines.pop(0) # the first rows are just the header and it will be removed
        rows = rows + lines
        random.shuffle(rows)
        for row in rows:
            rowLs = row.split(self.FS)
            if len(rowLs) > 5:
                list_of_list.append(row.split(self.FS))
        return list_of_list

    def _getPB(self, storyNum = 1):
        pbs = []
        contexts = ['N', 'P']
        random.shuffle(contexts)
        for context in contexts:
            for list in self._listOfList:
                if list[1] == 'PB' and list[3] == context:
                    self._listOfList.remove(list)
                    if storyNum == 2:
                        list[5] = list[7 + random.choice([0, 1])].rstrip("\n\r")
                    pbs.append(list)
                    break
        return pbs

    def _writeFile(self, listOfList, file_name):
        ouptup_file = codecs.open(file_name, 'a', encoding='utf-8')
        # if mode == 'w':
        if os.stat(file_name).st_size == 0:
            ouptup_file.write(self._arguments_header)
        try:
            for list in listOfList:
                ouptup_file.write(self.FS.join(list))
        finally:
            ouptup_file.close()

    # 8 stories (goodStories) taken from the first part of the experiemnt
    # record_answer (-+) 4 (--) / 4 (+-) 4 (++)
    # record_answer (N1) 4 (N0) / 4 (P0) 4 (P1)
    def getStoriesFromResponse(self):
        lines = self._getLines(self.outputFiles[2])[2:] # the first two lines are useless because they are PB
        # random.shuffle(lines)
        contextsVsTargetWords = [['N', 1], ['N', 0], ['P', 0], ['P', 1]]
        goodStories = []
        for ctxVsTW in contextsVsTargetWords:
            countCtxVsTW = 0
            for row in lines:
                rowLs = row.split(self.FS)
                if ctxVsTW[0] == rowLs[1] and ctxVsTW[1] == int(rowLs[2]):
                    if countCtxVsTW == 4:
                        continue
                    goodStories.append(rowLs[0] + '.' + rowLs[2])
                    countCtxVsTW += 1
                    if len(goodStories) >= self.MAX_GOOD_STORIES:
                        return goodStories
        return goodStories

    def record_answer(self, uid, context, key_resp_1):
        ouptup_file = open(self.outputFiles[2], 'a')
        if self.uui_check == uid :
            return;
        else:
            self.uui_check = uid
        try:
            _string = str(uid) + self.FS + context + self.FS + str(key_resp_1) + '\n'
            ouptup_file.write(_string)
        finally:
            ouptup_file.close()

    def _getLines(self, fileName):
        # TODO
        if len(self._openFile(fileName).readlines()[-1]) > 2:
            return self._openFile(fileName).readlines()
        else:
            return self._openFile(fileName).readlines()[:-1]

    def _getInt(self, _string):
        return int(_string.split('.')[0])

    def _getRsp(self, _string):
        return int(_string.split('.')[1])

    def _openFile(self, fileName):
        return codecs.open(os.path.realpath(fileName), encoding='utf-8')

    def _removeFiles(self, files):
        for file in files:
            if os.path.isfile(file):
                os.remove(file)

    def _doubleStories(self, stories):
        doubledStories = []
        for story in stories:
            storyLs = story.split(self.FS)
            for i in range(0, 2):
                storyLs[5] = storyLs[7 +i].rstrip("\n\r")
                doubledStories.append(storyLs)
        return doubledStories

    #used by test.py
    def fakeResponse(self, data):
        for responses in data:
            self.record_answer(responses[0], responses[1], responses[2])
