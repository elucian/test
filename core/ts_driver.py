from core import ts_config, ts_keyword, ts_reporter

import sys
import re

from datetime import datetime, timedelta

# Global driver options
main_action   = "execute"
next_action   = "continue"
break_case    = None
report        = None

# Debug mode actions for driver
actions     = ["break","skip","next","resume","exit"]

# Main action is set from run parameters to : execute, check, debug
# Actually command running is happening only in execute mode
def set_main_action(action):
   global main_action
   main_action = action

def set_next_action(action):
   global next_action
   next_action = action
   
def set_break_case(cfg,case_code):
   global break_case
   if case_code:
      cfg.check_code(case_code)
   break_case = case_code

#ask the user for next action in debug mode
def read_action():
    action = 'none'
    while action not in actions:
          action = raw_input("action:>")
          if action not in actions:
                print ('enter one of:',actions)
    return action

# create a report for this session (singleton)
def start_report(cfg, log):
    global report
    report = ts_reporter.mem_report(cfg)
    report.start()
    log.info('Report name is: %s' % report.file_name)

# close the report file and returns
def close_report():
    if report:
       report.close()

# ask user for the break code when next action is beak
def read_break(cfg):
    while True:
       break_code = raw_input("break code:>")
       try:
         set_break_case(cfg,break_code)
         return break_code
       except Exception as details:
         print(details)

# Function run_case is recursive
# Run a script or a test case
def run_case(cfg, log):
    cfg.set_execute(main_action,next_action)
    caseCount   = 0
    caseFail    = 0
    totalCount  = 0
    totalFail   = 0
    previous_case = None
    while True:
       test_case = next_case(cfg,log,previous_case)
       test_code = cfg.test_code
       #prepare next iteration
       previous_case = test_case
       # Infinite loop exit contiditon
       if not test_case :break

       # Check the break case for debug
       if (main_action in ('debug','check') and next_action in ('next','skip') or break_case and (
           (test_case.code == break_case) or
           (test_code+'.'+test_case.code == break_case) or
           (main_action in ('check','debug') and '+' in break_case and re.match(break_case,test_case.code)) or
           (main_action in ('check','debug') and '+' in break_case and re.match(break_case,test_code+'.'+test_case.code))
          )):
           # debug mode read for next action
           log.info('next case "%s.%s"' % (test_code,test_case.code))
           if  main_action in ['debug','check']:
               set_next_action(read_action())
               if next_action == "break":
                  read_break(cfg)
                  set_next_action("continue")
               else:
                  set_break_case(cfg,None)
           elif main_action == "execute":
              # break point, stop execution
              set_next_action("exit")
           elif main_action == "resume" :
              set_next_action("resume")
           cfg.set_execute(main_action,next_action)
           
       # user choose to resume execution, we change the main action to execute
       if next_action == "skip":
          log.info('user skip case "%s.%s"' % (test_code,test_case.code))
          if report: report.csv_row(test_case)
          continue
       if next_action == "exit":
          log.warning("system force exit")
          if report: report.csv_row(test_case)
          sys.exit(3);
       if test_case.status in ('disable','disabled'):
          log.warning('Case "%s" is disabled:' % test_case.code)
          test_case.status='disable'
          if report: report.csv_row(test_case)
          continue
       # Log header for test script
       # check if test is a script
       caseCount +=1
       if test_case.keyword =='include':
          print_separator(log)
          #flush report cahce into file
          if report:report.flush_file()
          #store previous case into local variable for next iteration
          script_file   = test_case.get_arg('script')
          log.info('next script: %s' % script_file)
          config_obj  = ts_config.config_parser(script_file,'unspecified',cfg,test_case)
          config_obj.set_execute(main_action,next_action)
          test_case.start_case()
          #define variables first time
          cFail      = 0 # Number of failures
          cCount     = 0 # Number of cases
          #try to execute each case and count errors
          try:
              ts_config.checkFolders(config_obj)
              cCount, cFail = run_case(config_obj, log)
          except Exception as detail:
             cFail      = 1
             cCount     = 1
             log.critical('errors in test case "%s"' % test_case.code)
             log.critical(detail)
             if main_action in ('debug','check'):
                raise
          finally:
             # log statistics
             if cFail!=0:
                 status='fail'
             else:
                 status='pass'
             #prepare statistics
             test_case.end_case(status)
             print_separator(log)
             log.info("active cases: #%s failing cases: #%s " % (cCount,cFail))
             if test_case.status == 'fail':
                 caseFail  +=1
                 log.error('script "%s" %s' % (test_case.code, test_case.status))
             else:
                 log.info('script "%s" %s' % (test_case.code, test_case.status))
             #register test case status and report
       else:
          # then call the proper keyword for the test_case object
          # log.info("next case: %s" % test_case.code)
          try:
             status    = run_test(cfg, log, test_case)
          except Exception as detail:
             status='error'
             log.critical('errors in test case "%s"' % test_case.code)
             log.critical(detail)
             if main_action in ('debug','check'):
                raise
          finally:
             test_case.end_case(status)
             if test_case.status in ['fail','critical','error']:
                caseFail +=1
                log.error('case %s in (%s)' % (status, test_case.duration))
             elif test_case.keyword !='log':
                log.info('case %s in (%s)' % (status, test_case.duration))
             if report:
                report.csv_row(test_case)                
    #end while
    return caseCount, caseFail
#end run_case

# Function run_test execute on single test case
# Can execute any keyword except a test script
def run_test(cfg, log, test_case):
    global main_action
    return_code = 0
    errorCount  = 0
    # on console every test_case is separated by a line from previous test_case
    if test_case.keyword !='log':
       print_separator(log)
    # ask user for next action in case of debug
    # try to execute or check the test case
    test_case.start_case()
    if cfg.execute:
       action = 'execute'
    else:
       action = 'verify'
    # log first message for test case
    if test_case.keyword!='log':
       log.info('%s case: "%s.%s"' % (action,cfg.test_code,test_case.code))
    # Check keyword to exist in registry
    if test_case.keyword not in ts_keyword.registry:
       log.error('Unknown keyword "%s" in "%s"' % (test_case.keyword,test_case.code))
       return 'error'          
    #check if all variables have been replaced
    try:
       test_case.check_prepared()
    except Exception as detail:
       log.error(detail)
       errorCount +=1
       if main_action in ('debug','check'):
          raise

    # execute or check a keyword command
    log.debug('keyword = %s', test_case.keyword)
    command     =  ts_keyword.registry.get(test_case.keyword)
    return_code =  command(cfg,log,test_case)

    # verify the exit condition and count the errors
    if (return_code!=0): errorCount +=1

    # for non log tasks we log the return code
    if errorCount == 0 and cfg.execute:
       status = 'pass'
    elif errorCount == 0:
       status = 'valid'
    else:
       status = 'fail'
    #end "while" loop
    return status
#end run_test

#get the next case looking at current_case status and options
def next_case(cfg,log,current_case):
    when_pass = cfg.when_pass
    when_fail = cfg.when_fail
    next_case = None
    # read in-line options for current case
    if current_case:
       when_pass = current_case.when_pass
       when_fail = current_case.when_fail
       # verify curent case status
       if  current_case.status=='pass' and current_case.when_pass == 'exit':
           log.warning('Exit due to condition: when_pass="exit"')
           return None
       if  current_case.status in ('fail','error') and current_case.when_fail == 'exit':
           log.warning('Exit due to condition: when_fail="exit"')
           return None
       # analyze the if a loop is active stay on same case until is loop finished
       if current_case.has_arg('loop_config') and current_case.next_loop >= 0: 
          next_case=current_case.code

    # verify if next case is correct in the script
    if when_pass not in ('next','exit'):
       assert when_pass in cfg.test_list ,'Incorect option when_pass = "%s"' % when_pass
    if when_fail not in ('next','exit'):
       assert when_fail in cfg.test_list ,'Incorect option when_fail = "%s"' % when_fail
    # Get the next case from iterator
    if not next_case:
       try:
          next_case = cfg.iterator.next()
          # Suport for jumping ahead test cases. Jump back is not possible my design
          # We can specify when_pass=<case_code> or when_fail=<case_code>
          if current_case:
             if current_case.status=='pass' and when_pass not in ['next','exit']:
                while next_case and next_case != when_pass:
                   next_case = cfg.iterator.next()
             if current_case.status in ('fail','error') and when_fail not in ['next','exit']:
                while next_case and next_case != when_fail:
                   next_case = cfg.iterator.next()
       except:
          next_case = None
    # Prepare variables of next_case
    if next_case:
       # replace variables in argument of type dictionary
       result = cfg.test_cases[next_case]
       # Inject variables from case into configuration using @var = value notation
       cfg.update_var_case(result)
       # start loop or prepare next loop if looper already started
       if result.has_arg('loop_config'):
          if result.next_loop==0:
             result.loop_config=cfg.replace_variables(result.argument['loop_config'])
             result.start_loop()
          result.set_loop_args()
       # synchronize next case arguments (elinimane ${} placeholders)
       result.refresh_arguments()
       # replace variables in argument of type list
       result.refresh_parameters()
       # prepare next case arguments with variables from config 
       for key, value in result.argument.iteritems():
           result.argument[key]=cfg.replace_variables(value)
       # replace variables in argument of type list
       for i in range(len(result.params)):
           result.params[i]=cfg.replace_variables(result.params[i])
    else:
       result=None
    return result
#end next_case


def print_separator(log):
    log.info('-' * 80)

#end