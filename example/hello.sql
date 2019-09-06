-- Script to demonstrate PL/SQL call                          
whenever sqlerror exit failure
whenever oserror  exit failure
                          
select 'hello world' from dual;


exit;
/