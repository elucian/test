select message
from shd_val_report  
where rule_id = '${rule_id}' and id = 0;

select message
from shd_val_report  
where rule_id = '${rule_id}' and id > 0;
