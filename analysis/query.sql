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
    and stimuli.sentence_block != 'PB' AND irony_type = 'S'
GROUP BY user_id;

