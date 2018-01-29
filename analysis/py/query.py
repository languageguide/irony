
class Query():

    def get_query(self, context, user_response):
        return '''
            SELECT user.id, count(stimuli.id)
            FROM user
            LEFT JOIN trials_1 ON trials_1.user_id = user.id and trials_1.user_response = '%s'
            LEFT JOIN stimuli ON stimuli.id = trials_1.stimuli_id and stimuli.context = '%s' and stimuli.sentence_block != 'PB'
            GROUP BY user_id;
        ''' % (user_response, context)

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
