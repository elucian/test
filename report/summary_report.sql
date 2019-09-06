select   category
        ,vr.rule_id
        ,rule_desc
        ,decode(vs.mseverity, 1, 'Fatal', 2, 'Critical', 3, 'Error', 'Warning') as severity
        ,decode(vr.status, 'E', 'Enabled', 'D', 'Disabled') as status
        ,nvl(cnt.fail, 0) as fail_count
    from pipeline_val_rule vr
        ,(select vss.rule_id, max(vss.severity) mseverity from pipeline_val_severity vss group by rule_id) vs 
        ,(select count(*) as fail
                ,rule_id
            from pipeline_val_exception
           group by rule_id) cnt
   where vr.rule_id = vs.rule_id
     and vr.rule_id = cnt.rule_id(+)
   order by category
           ,rule_id;
