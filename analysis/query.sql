select
user.id,
count(stimuli.id) 
from
user
LEFT JOIN trials_1 on trials_1.user_id = user.id and trials_1.user_response = 'NA'
LEFT JOIN stimuli on stimuli.id = trials_1.stimuli_id and stimuli.context = 'P' and stimuli.sentence_block != 'PB'
group by user_id;




select
count(stimuli.id)
from
stimuli, trials_1
where
stimuli.id = trials_1.stimuli_id and
trials_1.user_response = 'NA' and
stimuli.context = 'N' and
stimuli.sentence_block != 'PB';


get_trials1_by_context_ironyType


select
stimuli.context, trials_1.user_response , count(stimuli.id)
from
stimuli, trials_1
where
stimuli.id = trials_1.stimuli_id and
-- trials_1.user_response = 'NA' and
-- stimuli.context = 'N' and
stimuli.sentence_block != 'PB';


select
user_id,
count(stimuli.id) 
from
stimuli, trials_1, user 
where
stimuli.id = trials_1.stimuli_id and
trials_1.user_id = user.id and
trials_1.user_response = 'NA' and
stimuli.context = 'P' and
stimuli.sentence_block != 'PB'  
group by user_id;


select user.id, count(user.id)
from
 user
  left outer join  
  left outer join trials_1 on trials_1.user_response = 'NA' and trials_1.user_id = user.id and stimuli.id = trials_1.stimuli_id
group by user.id;

select
user.id,
count(user.id) 
from
stimuli, user 
left outer join trials_1 on stimuli.id = trials_1.stimuli_id and trials_1.user_id = user.id and trials_1.user_response = 'NA'
where
-- stimuli.id = trials_1.stimuli_id and
-- trials_1.user_id = user.id and
-- trials_1.user_response = 'NA' and
stimuli.context = 'P' and
stimuli.sentence_block != 'PB'  
group by user.id;


SELECT  context, irony_type, trials_1.user_response, COUNT(trials_1.id)
FROM trials_1, stimuli, user WHERE
sentence_block != 'PB' AND
user.id = trials_1.user_id AND
age <> '68' AND
stimuli_id = stimuli.id GROUP BY context, irony_type, trials_1.user_response;


SELECT user.id, count(stimuli.id)
FROM user
LEFT JOIN trials_1 
    ON trials_1.user_id = user.id and trials_1.user_response = 'PA'
LEFT JOIN stimuli ON 
    stimuli.id = trials_1.stimuli_id and stimuli.context = 'P' 
    and stimuli.sentence_block != 'PB' AND irony_type = 'I'
GROUP BY user_id;

SELECT
    user.id,
    count(trials_1.user_id),
    -- context,
    trials_2.user_response = trials_1.user_response AS correct,
    stimuli.target_word_p = missing_TW as isPositive
FROM
    user
LEFT JOIN trials_1
    ON
        user.id = trials_1.user_id
LEFT JOIN trials_2
    ON
        trials_1.user_id = trials_2.user_id AND
        trials_1.stimuli_id = trials_2.stimuli_id
LEFT JOIN stimuli
    ON
        correct = 0 AND
        sentence_block != 'PB' AND
        context = 'N' AND
        stimuli.id = trials_1.stimuli_id AND
        stimuli.id = trials_2.stimuli_id
GROUP BY
    trials_1.user_id;

SELECT
    user.id,
    stimuli.irony_type,
    count(stimuli.id)
FROM
    user, trials_1, trials_2, stimuli
WHERE
    user.id = trials_1.user_id AND
    trials_1.user_id = trials_2.user_id AND
    trials_2.user_response != trials_1.user_response AND
    trials_1.stimuli_id = trials_2.stimuli_id AND
    sentence_block != 'PB' AND
    context = 'N' AND
    stimuli.id = trials_1.stimuli_id AND
    stimuli.id = trials_2.stimuli_id AND
    stimuli.target_word_p != missing_TW
GROUP BY trials_1.user_id, stimuli.irony_type;



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
        stimuli.target_word_p == missing_TW --to change
GROUP BY trials_1.user_id;


SELECT
    user.id,
    count(stimuli.id),
    context, 
    stimuli.irony_type
FROM
    user, trials_1, trials_2, stimuli
WHERE 
    user.id = trials_1.user_id AND
    trials_1.user_id = trials_2.user_id AND
    trials_2.user_response != trials_1.user_response AND
    trials_1.stimuli_id = trials_2.stimuli_id AND 
    sentence_block != 'PB' AND 
    context = 'N' AND 
    stimuli.id = trials_1.stimuli_id AND 
    stimuli.id = trials_2.stimuli_id AND
    stimuli.target_word_p != missing_TW AND --variable 0/1
    stimuli.irony_type = 'I' -- variable I/S
GROUP BY
    trials_1.user_id;

--- ---------------
-------------------

SELECT
    user.id,
    count(stimuli.id)
FROM
    user, trials_1, trials_2, stimuli
WHERE 
    user.id = trials_1.user_id AND
    trials_1.user_id = trials_2.user_id AND
    trials_2.user_response != trials_1.user_response AND
    trials_1.stimuli_id = trials_2.stimuli_id AND 
    sentence_block != 'PB' AND 
    context = 'N' AND 
    stimuli.id = trials_1.stimuli_id AND 
    stimuli.id = trials_2.stimuli_id AND
    stimuli.target_word_p != missing_TW AND --variable 0/1
    stimuli.irony_type = 'I' -- variable I/S
GROUP BY
    trials_1.user_id;
----------------------

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
        context = 'N' AND 
        stimuli.id = trials_1.stimuli_id AND 
        stimuli.id = trials_2.stimuli_id AND
        stimuli.target_word_p == missing_TW AND --variable 0/1
        stimuli.irony_type = 'S' -- variable I/S
GROUP BY
    trials_1.user_id;
    


