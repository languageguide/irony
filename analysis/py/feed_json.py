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

    def __get_tr1_tr2_header(self, value):
        translated_value = {
            '==': 'is positive',
            '!=': 'is not positive'
        }
        return translated_value[value]

    def __get_tr1_tr2_IT_header(self, value):
        translated_value = {
            'P==I': 'PosCont, is positive, Ironic',
            'P!=I': 'PosCont, is not positive, Ironic',
            'P==S': 'PosCont, is positive, Sarcastic',
            'P!=S': 'PosCont, is not positive, Sarcastic',
            'N==I': 'NegCont, is positive, Ironic',
            'N!=I': 'NegCont, is not positive, Ironic',
            'N==S': 'NegCont, is positive, Sarcastic',
            'N!=S': 'NegCont, is not positive, Sarcastic'
        }
        return translated_value[value]

    def __get_negContVsPosCont_header(self, value):
        translated_value = {
            'P': 'PosCont',
            'N': 'NegCont'
        }
        return translated_value[value]

    def set_summary(self):
        # query to get the summary
        json_data = {}
        for r in self.conn.execute(self.query.get_summary_trials1()).fetchall():
            json_data[self.__get_summary_value(r[0] + r[1])] = r[2]
        self.__write_json_file('summary.json', json_data)

    def set_summary_trials1_by_context_ironyType(self):
        json_data = {}
        for r in self.conn.execute(self.query.get_trials1_data_sql()).fetchall():
            json_data[self.__get_trials1_header(r[0] + r[1] + r[2])] = r[3]
        self.__write_json_file('trials1_data.json', json_data)

    def get_trials1_response(self):
        # query to get the users' responses divided by stimuli-context and trials_1-user_response
        tr1_resp = {}
        for context in ['P', 'N']:
            for user_response in ['PA', 'NA']:
                query = self.query.get_trials1_response_sql(context, user_response)
                # TODO self.conn.execute(query).fetchall() should be a private method
                tpls = self.conn.execute(query).fetchall()
                tr1_resp[self.__get_summary_value(context + user_response)] = [x[1] for x in tpls]
        self.__write_json_file('userResponse.json', tr1_resp)
        return tr1_resp

    def get_trials1_by_ironyType(self):
        tr1_resp = {}
        for context in ['P', 'N']:
            for user_response in ['PA', 'NA']:
                for ironyType in ['I', 'S']:
                    query = self.query.get_trials1_by_ironyType_sql(context, user_response, ironyType)
                    # TODO self.conn.execute(query).fetchall() should be a private method
                    tpls = self.conn.execute(query).fetchall()
                    tr1_resp[self.__get_trials1_header(context + ironyType + user_response)] = [x[1] for x in tpls]
        self.__write_json_file('userResponseByIronyType.json', tr1_resp)
        return tr1_resp

    def get_tr1_tr2_by_TW(self):
        tr1_resp = {}
        for missing_TW in ['==', '!=']:
            query = self.query.get_tr1_tr2_by_TW_sql(missing_TW)
            print query
            # TODO self.conn.execute(query).fetchall() should be a private method
            tpls = self.conn.execute(query).fetchall()
            tr1_resp[self.__get_tr1_tr2_header(missing_TW)] = [x[1] for x in tpls]
        return tr1_resp

    def get_tr1_tr2_by_TW_IT(self):
        tr1_resp = {}
        for missing_TW in ['==', '!=']:
            for irony_type in ['I', 'S']:
                for context in ['P', 'N']:
                    query = self.query.get_tr1_tr2_by_TW_IT_sql(context,missing_TW, irony_type)
                    tpls = self.conn.execute(query).fetchall()
                    tr1_resp[self.__get_tr1_tr2_IT_header(context + missing_TW + irony_type)] = [x[1] for x in tpls]
        return tr1_resp

    def get_negContVsPosCont(self):
        tr1_resp = {}
        for context in ['P', 'N']:
            query = self.query.get_negContVsPosCont_sql(context)
            print query
            tpls = self.conn.execute(query).fetchall()
            tr1_resp[self.__get_negContVsPosCont_header(context)] = [x[1] for x in tpls]
        return tr1_resp

    def set_ttest_response(self, series, file_name):
        # Method to get the t-test between two samples
        from scipy.stats import ttest_ind
        from numpy import mean, std
        from itertools import combinations
        import numpy as np
        from math import isnan
        tr1_tt = {'data': []}
        for key1 in series:
            for key2 in series:
                if key1 != key2:
                    mean1 = round(mean(series[key1]), 2)
                    mean2 = round(mean(series[key2]), 2)
                    std1 = round(std(series[key1]), 2)
                    std2 = round(std(series[key2]), 2)
                    if mean1 != 0 and mean2 != 0:
                        t, p = ttest_ind(series[key1], series[key2], equal_var=True)
                        t = round(t, 5)
                        p = round(p, 5)
                    else:
                        t = "NaN"
                        p = "NaN"
                    tr1_tt['data'].append([key1, key2, t, p, mean1, std1, mean2, std2])
        self.__write_json_file(file_name, tr1_tt)

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
feedJson.set_ttest_response(feedJson.get_trials1_response(), 'ttest.json')
feedJson.set_ttest_response(feedJson.get_trials1_by_ironyType(), 'ttestByIronyType.json')
feedJson.set_ttest_response(feedJson.get_tr1_tr2_by_TW(), 'ttest_tr1_tr2.json')
feedJson.set_ttest_response(feedJson.get_tr1_tr2_by_TW_IT(), 'ttest_tr1_tr2_ironyType.json')
feedJson.set_ttest_response(feedJson.get_negContVsPosCont(), 'negContVsPosCont.json')
feedJson.set_correct_responses()
feedJson.set_correct_responses_by_context()
feedJson.set_correct_responses_by_irony()

