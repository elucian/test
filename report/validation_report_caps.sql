select message
from shd_val_report  
where rule_id = '${RULE_ID}' and id = 0;

select message
from shd_val_report  
where rule_id = '${RULE_ID}' and id > 0;
