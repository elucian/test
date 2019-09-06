#!/usr/local/bin/python
# This is the startup script for Pipeline Test Automation (PTA) framework
# Created by Elucian Moise at 27 June 2011

# Python standard libraries
import sys
import os
import platform
import argparse

from datetime import datetime

# Extended libraries
from core import *

# User can specify one main action: [execute, check, debug]
actions = {"execute", "resume", "check", "debug"}

def main():
    """ This is the main procedure for PTA application"""
    parser = argparse.ArgumentParser(description='PTA framework version 1.0 Copyright NAVTEQ 2011.',
                               epilog='This is how you use the PTA framework')

    parser.add_argument('test_suite',
                             help='Test scrip file including path.',
                             metavar='<test_scrip>'
                             )

    parser.add_argument('-c','--config',
                             help='Config folder (optional)',
                             metavar='<config_param>',
                             required=False,
                             default = 'unspecified',
                             dest='config_param'
                             )
							 
    parser.add_argument('-a','--action',
                             help='Main action: "execute","resume","check","debug" (optional)',
                             metavar='<main_action>',
                             required=False,
                             default = 'execute',
                             dest='main_action'
                             )
							 
    parser.add_argument('-b','--break',
                             help='Specify break case (optional)',
                             metavar='<break_case>',
                             required=False,
                             default = None,
                             dest='break_case'
                             )

    parser.add_argument('-n','--number',
                             help='Build number',
                             metavar='<build_number>',
                             required=False,
                             default = None,
                             dest='build_number'
                             )

    parser.add_argument('-l','--location',
                             help='artifacts location',
                             metavar='<artifact_location>',
                             required=False,
                             default = None,
                             dest='artifact_location'
                             )
                             
    args = parser.parse_args()
      
    # record the start time
    start_time = datetime.now()

    # check if main action is provided
    if args.main_action not in actions:
       parser.error('invalid value provided for action argument')

    #detect fle type suite or script
    if args.test_suite[-7:]=='.script': 
       test_type = 'script'      
    elif args.test_suite[-6:]=='.suite':
       test_type = 'suite'
    else:
       parser.error('Wrong file extension: %s' %  args.test_suite)
       
    # check if configuration file is provided
    test_suite = os.path.normpath(args.test_suite)
    if not os.path.exists(test_suite):
       parser.error('Test file not found: %s' % test_suite)
    
    # parse configuration file
    if args.build_number:
       ts_config.set_build_number(args.build_number)

    # set the artifact location
    if args.artifact_location:
       ts_config.set_artifact_loc(args.artifact_location)     
       
    config_obj = ts_config.config_parser(test_suite,args.config_param)

    # set debuging cases (all of them are optional)
    ts_driver.set_main_action(args.main_action)
    ts_driver.set_break_case(config_obj,args.break_case)

    # verify configuration folders
    ts_config.checkFolders(config_obj)

    # create the log file
    log = ts_loger.setupLog(config_obj,args.main_action)

    log.info('=' * 80)
    if args.main_action == 'execute':
        log.info('Executing PTA please wait...')
    if args.main_action == 'resume':
        log.info('Resuming PTA please wait...')
    if args.main_action == 'check':
        log.info('Checking PTA configuration please wait...')
    if args.main_action == 'debug':
        log.info('Debuging PTA ...')
    log.info('=' * 80)


    # configuration short report
    log.info('Computer name : %s' % platform.node())
    log.info('User name     : %s' % config_obj.get_var('USER_NAME'))
    log.info('Runtime folder: %s' % config_obj.runtime_folder)
    log.info('Output folder : %s' % config_obj.output_folder)
    
    # establish working directory
    os.chdir(config_obj.runtime_folder)

    # first log message
    log.info('Test %s    : %s '  % (test_type,args.test_suite))
    log.info('Description   : %s '  % config_obj.description)
    log.info('Main action   : %s' % args.main_action)    
    log.info('Start time    : %s '  % str(start_time))
    if args.break_case:
       log.info('Break case    : %s' % args.break_case)        
    log.info('=' * 80)

    # create report variable
    if config_obj.has_var('REPORT_FILE'):
       ts_driver.start_report(config_obj, log)
    else:
       log.warning('Report is not created. Variable REPORT_FILE not defined!')   

    if not config_obj.has_var('XML_FILE'):
       log.warning('XML Report is not created. Variable XML_FILE not defined!')   

    # establish the next action for debug mode with no beack
    if args.main_action=='debug' and not args.break_case:
       ts_driver.set_next_action('next')
    # execute or check every test case listed in test script
    scrptCount, scriptFail = ts_driver.run_case(config_obj, log)
    
    # close the report file and flush last records to disk
    ts_driver.close_report()

    # prepare end of script
    end_time  = datetime.now()
    exec_time = end_time - start_time

    # convert CSV file into XML
    if ts_driver.report and config_obj.has_var('XML_FILE'):
       ts_driver.report.build_xml(scrptCount,scriptFail,exec_time)       

    # short statistic about test
    log.info('=' * 80)
    log.info('Test %s    : %s '  % (test_type,args.test_suite))
    log.info('Description   : %s '  % config_obj.description)
    log.info('Main action   : %s' % args.main_action)    
    log.info('Start time    : %s '  % str(start_time))	
    log.info('User name     : %s' % config_obj.get_var('USER_NAME'))
    log.info('Runtime folder: %s' % config_obj.runtime_folder)
    log.info('Output folder : %s' % config_obj.output_folder)
    log.info('=' * 80)
    log.info('End test at: %s' % str(end_time))
    log.info('Total time: %s' % str(exec_time))
    if scriptFail == 0:
       log.info('Action: %s pass for %s: "%s" ' % (args.main_action, test_type, config_obj.test_name))
    else:       
       log.error('Action: %s fail for %s: "%s"' % (args.main_action, test_type, config_obj.test_name))   
       log.error('Total cases in %s : #%d, failing cases #%d ' % (test_type, scrptCount, scriptFail))
    log.info('=' * 80)


    # exit code 1 when not all scripts are passing
    if scriptFail != 0: sys.exit(1)
#end main()

     
if __name__ == '__main__':
  main()
