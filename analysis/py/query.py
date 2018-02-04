
class Query():

    def get_trials1_liter_vs_ironic_sql(self, opts):
        return '''
            SELECT
                user.id, count(stimuli.id)
            FROM
                user
            LEFT JOIN trials_1
                ON
                    trials_1.user_id = user.id
            LEFT JOIN stimuli
                ON
                    stimuli.id = trials_1.stimuli_id AND
                    stimuli.sentence_block != 'PB' AND
                (
                    (stimuli.context = '%s' AND trials_1.user_response = '%s' )
                        OR
                    (stimuli.context = '%s' AND trials_1.user_response = '%s' )
                )
            GROUP BY user_id;
        ''' % (opts[0], opts[1], opts[2], opts[3])

    def get_trials1_response_sql(self, context, user_response):
        return '''
            SELECT user.id, count(stimuli.id)
            FROM user
            LEFT JOIN trials_1 ON trials_1.user_id = user.id and trials_1.user_response = '%s'
            LEFT JOIN stimuli ON stimuli.id = trials_1.stimuli_id and stimuli.context = '%s' and stimuli.sentence_block != 'PB'
            GROUP BY user_id;
        ''' % (user_response, context)

    def get_trials1_by_ironyType_sql(self, context, user_response, ironyType):
        return '''
            SELECT user.id, count(stimuli.id)
            FROM user
            LEFT JOIN trials_1 
                ON trials_1.user_id = user.id and trials_1.user_response = '%s'
            LEFT JOIN stimuli ON 
                stimuli.id = trials_1.stimuli_id and stimuli.context = '%s' 
                and stimuli.sentence_block != 'PB' AND irony_type = '%s'
            GROUP BY user_id;
        ''' % (user_response, context, ironyType)

    def get_tr1_tr2_by_TW_sql(self, missing_TW):
        return '''
            SELECT
                user.id,
                count(stimuli.id)
            FROM
                user
            LEFT JOIN trials_1
                ON
                    user.id = trials_1.user_id
            LEFT JOIN trials_2
                ON
                    trials_1.user_id = trials_2.user_id AND
                    trials_2.user_response != trials_1.user_response AND
                    trials_1.stimuli_id = trials_2.stimuli_id
            LEFT JOIN stimuli
                ON
                    stimuli.sentence_block != 'PB' AND
                    stimuli.context = 'N' AND
                    stimuli.id = trials_1.stimuli_id AND
                    stimuli.id = trials_2.stimuli_id AND
                    stimuli.target_word_p %s missing_TW --to change
            GROUP BY trials_1.user_id;
        ''' % (missing_TW)

    def get_tr1_tr2_by_TW_IT_sql(self, context, missing_TW, irony_type):
        return '''
            SELECT
                user.id,
                count(stimuli.id)
            FROM
                user
            LEFT JOIN trials_1
                ON 
                    user.id = trials_1.user_id
            LEFT JOIN trials_2
                ON 
                    trials_1.user_id = trials_2.user_id AND
                    trials_2.user_response != trials_1.user_response AND
                    trials_1.stimuli_id = trials_2.stimuli_id
            LEFT JOIN stimuli
                ON 
                    sentence_block != 'PB' AND 
                    context = '%s' AND 
                    stimuli.id = trials_1.stimuli_id AND 
                    stimuli.id = trials_2.stimuli_id AND
                    stimuli.target_word_p %s missing_TW AND --variable 0/1
                    stimuli.irony_type = '%s' -- variable I/S
            GROUP BY
                trials_1.user_id;
        ''' % (context, missing_TW, irony_type)

    def get_correct_responses_sql(self):
        return '''
            SELECT  count(trials_1.user_id), trials_2.user_response = trials_1.user_response AS correct
            FROM trials_1, trials_2, stimuli
            WHERE trials_1.user_id = trials_2.user_id and
            trials_1.stimuli_id = trials_2.stimuli_id
            and stimuli.id = trials_1.stimuli_id
            and stimuli.id = trials_2.stimuli_id group by correct;
        '''

    def get_correct_responses_by_context_sql(self):
        return '''
            SELECT  count(trials_1.user_id), context, trials_2.user_response = trials_1.user_response AS correct
            FROM trials_1, trials_2, stimuli
            WHERE trials_1.user_id = trials_2.user_id
            and trials_1.stimuli_id = trials_2.stimuli_id
            and sentence_block != 'PB'
            and stimuli.id = trials_1.stimuli_id
            and stimuli.id = trials_2.stimuli_id group by context, correct;
        '''

    def get_correct_responses_by_irony_sql(self):
        return '''
            SELECT  count(trials_1.user_id), irony_type, trials_2.user_response = trials_1.user_response AS correct
            FROM trials_1, trials_2, stimuli
            WHERE trials_1.user_id = trials_2.user_id and
            sentence_block != 'PB' and
            sentence_block != 'DISTR' and
            trials_1.stimuli_id = trials_2.stimuli_id
            and stimuli.id = trials_1.stimuli_id
            and stimuli.id = trials_2.stimuli_id group by irony_type, correct;
        '''

    def get_trials1_data_sql(self):
        return '''
            SELECT  context, irony_type, trials_1.user_response, COUNT(trials_1.id)
            FROM trials_1, stimuli, user WHERE
            sentence_block != 'PB' AND
            user.id = trials_1.user_id AND
            stimuli_id = stimuli.id GROUP BY context, irony_type, trials_1.user_response;
        '''

    def get_summary_trials1(self):
        return '''
            SELECT stimuli.context, trials_1.user_response , count(stimuli.id)
            FROM stimuli, trials_1
            WHERE stimuli.id = trials_1.stimuli_id and stimuli.sentence_block != 'PB'
            GROUP BY stimuli.context, trials_1.user_response;
        '''

    def get_negContVsPosCont_sql(self, context):
        return '''
            SELECT
                user.id,
                count(stimuli.id)
            FROM
                user
            LEFT JOIN trials_1 ON
                user.id = trials_1.user_id
            LEFT JOIN trials_2 ON
                trials_1.user_id = trials_2.user_id AND
                trials_1.stimuli_id = trials_2.stimuli_id AND
                trials_2.user_response != trials_1.user_response
            LEFT JOIN stimuli ON
                stimuli.sentence_block != 'PB' AND
                stimuli.id = trials_1.stimuli_id AND
                stimuli.context = '%s' AND
                stimuli.id = trials_2.stimuli_id
            GROUP BY
                trials_1.user_id;
        ''' % (context)
