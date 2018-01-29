from db_schema import Base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, text
import json, sys, os
from query import Query

class FeedJson:
    def __init__(self, db_name):
        # TODO; you should get the db name from a conf file
        db_file_name = 'irony.db'
        if os.path.isfile(db_file_name):
            engine = create_engine('///'.join(['sqlite:', db_file_name]))
        else:
            raise Exception('The following file %s does not exist: ' % db_file_name)

        Base.metadata.bind = engine
        DBSession = sessionmaker()
        DBSession.bind = engine
        session = DBSession()
        self.conn = engine.connect()
        self.query = Query()

    def __write_json_file(self, file_name, json_data):
        directory = '../json'
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open('/'.join([directory, file_name]), 'w')
        f.write(json.dumps(json_data))

    def __get_summary_value(self, value):
        translated_value = {
            'PPA': 'PosContext-PosAdjective',
            'NPA': 'NegContext-PosAdjective',
            'PNA': 'PosContext-NegAdjective',
            'NNA': 'NegContext-NegAdjective'
        }
        return translated_value[value]

    def __get_trials1_header(self, value):
        translated_value = {
            'NINA': 'N|I|NA',
            'NIPA': 'N|I|PA',
            'NSNA': 'N|S|NA',
            'NSPA': 'N|S|PA',
            'PINA': 'P|I|NA',
            'PIPA': 'P|I|PA',
            'PSNA': 'P|S|NA',
            'PSPA': 'P|S|PA'
        }
        return translated_value[value]

    def set_summary(self):
        # query to get the summary
        json_data = {}
        for r in self.conn.execute(self.query.get_summary_trials1()).fetchall():
            json_data[self.__get_summary_value(r[0] + r[1])] = r[2]
        self.__write_json_file('summary.json', json_data)

    def set_trials1_data(self):
        json_data = {}
        for r in self.conn.execute(self.query.get_trials1_data_sql()).fetchall():
            json_data[self.__get_trials1_header(r[0] + r[1] + r[2])] = r[3]
        self.__write_json_file('trials1_data.json', json_data)


    def set_user_response(self):
        # query to get the users' responses divided by stimuli-context and trials_1-user_response
        self.tr1_resp = {}
        for context in ['P', 'N']:
            for user_response in ['PA', 'NA']:
                query = self.query.get_query(context, user_response)
                # TODO self.conn.execute(query).fetchall() should be a private method
                tpls = self.conn.execute(query).fetchall()
                self.tr1_resp[self.__get_summary_value(context + user_response)] = [x[1] for x in tpls]
        self.__write_json_file('userResponse.json', self.tr1_resp)

    def set_ttest_response(self):
        # Method to get the t-test between two samples
        from scipy.stats import ttest_ind
        from itertools import combinations
        import numpy as np
        tr1_tt = {'data': []}
        print self.tr1_resp
        for key1 in self.tr1_resp:
            for key2 in self.tr1_resp:
                if key1 != key2:
                    t, p = ttest_ind(self.tr1_resp[key1], self.tr1_resp[key2], equal_var=True)
                    tr1_tt['data'].append([key1, key2, float(t), p])
        self.__write_json_file('ttest.json', tr1_tt)

    def set_correct_responses(self):
        response = {}
        for row in self.conn.execute(self.query.get_correct_responses_sql()).fetchall():
            if row[1] == 0:
                response['Diff-Resp'] = row[0]
            else:
                response['Same-Resp'] = row[0]
        self.__write_json_file('correctResponse.json', response)

    # TODO merge set_correct_responses_by_context with set_correct_responses
    def set_correct_responses_by_context(self):
        response = {}
        for row in self.conn.execute(self.query.get_correct_responses_by_context_sql()).fetchall():
            if row[2] == 0 and row[1] == 'N':
                response['Neg-Cont_Diff-Resp'] = row[0]
            if row[2] == 1 and row[1] == 'N':
                response['Neg-Cont_Same-Resp'] = row[0]
            if row[2] == 0 and row[1] == 'P':
                response['Pos-Cont_Diff-Resp'] = row[0]
            if row[2] == 1 and row[1] == 'P':
                response['Pos-Cont_Same-Resp'] = row[0]
        self.__write_json_file('correctResponseByContext.json', response)

    # TODO merge set_correct_responses_by_irony with set_correct_responses
    def set_correct_responses_by_irony(self):
        response = {}
        for row in self.conn.execute(self.query.get_correct_responses_by_irony_sql()).fetchall():
            if row[2] == 0 and row[1] == 'I':
                response['Ironic_Diff-Resp'] = row[0]
            if row[2] == 1 and row[1] == 'I':
                response['Ironic_Same-Resp'] = row[0]
            if row[2] == 0 and row[1] == 'S':
                response['Sarcastic_Diff-Resp'] = row[0]
            if row[2] == 1 and row[1] == 'S':
                response['Sarcastic_Same-Resp'] = row[0]
        self.__write_json_file('correctResponseByIrony.json', response)

feedJson = FeedJson('irony.db')
feedJson.set_summary()
feedJson.set_user_response()
feedJson.set_ttest_response()
feedJson.set_correct_responses()
feedJson.set_correct_responses_by_context()
feedJson.set_correct_responses_by_irony()
feedJson.set_trials1_data()
