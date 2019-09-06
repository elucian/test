import os
import subprocess
import csv
from core import ts_loger, ts_config
import cx_Oracle
# Every keyword has a procedure starting with 'key_'
# Keyword procedures must be registered to be used
# Registry: Is a variable at the end of this file

# Keywords are waiting for the process to finish 
# then pass control back to the driver

# For shell commands i will use the new subprocess.Popen 
#    to create a subprocess when run something outside python
# In case of memory issues, we can change bufsize for 
#    specific commands: bufsize=-1 it may help.
# popen(args,
#       bufsize=0,
#       executable=None,
#       stdout=None,
#       stderr=None,
#       preexec_fn=None,
#       close_fds=False,
#       shell=False,
#       cwd=None,
#       universal_newlines=False,
#       startupinfo=None,
#       creationflags=0)

# Open oracle connections and store connection
def set_connection(cfg,log,login):
    """Create a new oracle connection if one does not exit"""
    if login not in cfg.connections:
       try:
          cfg.connections[login] = cx_Oracle.connect(login)
          log.info('Connected to Oracle: "%s"' % login)
       except cx_Oracle.DatabaseError as detail:
          log.error('Wrong connection descriptor %s' % login)
          log.debug(detail)
          return None
    #new connection or existing connection
    return cfg.connections[login]
        

def close_connection(cfg,login):
    """Disconnect and remove oracle connection from pool"""
    if login in connections:
       cfg.connections[login].close
       del cfg.connections[login]
    
# oracle is using dbms_output for some procedures to log messages
# we can capture the messages using folowing procedure
def log_dbms(curs,cfg,step):
    """ Read the dbms_output for a plsql execution """
    statusVar = curs.var(cx_Oracle.NUMBER)
    lineVar   = curs.var(cx_Oracle.STRING)
    log_file_name  = ts_loger.get_file_name(cfg,step,'log')
    dbms_loger= ts_loger.openLog(log_file_name)
    count = 0
    while True:
        curs.callproc("dbms_output.get_line", [lineVar, statusVar])
        if statusVar.getvalue() != 0: 
           break
        count += 1    
        dbms_loger.writeln(lineVar.getvalue())
    dbms_loger.close()
    step.log_file_name = log_file_name;
#end log_dbms
    
def log_error(msg,cfg,step):
    """ Read the dbms_output for a plsql execution """
    log_file_name  = ts_loger.get_file_name(cfg,step,'err')
    err_loger= ts_loger.openLog(log_file_name)    
    err_loger.writeln(msg)
    err_loger.close()
    step.err_file_name = log_file_name
        
#end

# faster version for log_dmbs. not used.
def log_dbms2(curs,log):
    """ Read the dbms_output for a plsql execution """
    numLinesVar = curs.var(cx_Oracle.NUMBER)
    lineVar     = curs.arrayvar(cx_Oracle.STRING,10)
    while True:
        numLinesVar.setvalue(0,2)
        curs.callproc("dbms_output.get_lines", [lineVar, numLinesVar])
        numLines=int(numLinesVar.getvalue())
        if numLines== 0:
           break
        for line in lineVar.getvalue()[:numLines]:
           log.debug(line)
#end log_dbms2

def key_log(cfg,log,step):
    """log a user message into the test suite log"""
    # expected 2 parameters: (type, message)
    assert step.argument.has_key("type"), 'argument "severity" must be provided'
    assert step.argument.has_key("message"),  'argument "message"  must be provided'
    type  = step.argument.get('type')
    assert type in ('info','error','warning','debug','critical'), 'Invalid type value "%s"' % type
    message  = step.argument.get('message')
    command  = "log.%s(%s)" % (type,message)
    log.debug('command: %s' % command)   
    if cfg.execute: 
       eval(command)
    return 0 #logging the message is successful
#end key_log

def key_shell(cfg,log,step):
    """run shell command, script or batch file using shell"""
    # OS path is used to search a specific command if not in current folder
    # Expected one argument "command" all other are separated by | or not
    if step.argument.has_key('command'):
       command = step.argument.get('command')
    else:
       command = step.params.pop(0)
    # add the run folder if specified
    command_arg = '%s %s' %(command,' '.join(step.params))
    return run_command(cfg,log,step,cfg.runtime_folder,command_arg,True)
#end shell

def key_run(cfg,log,step):
    """run batch process from bin folder if not other is specified """
    # Command is searched and run from BIN_FOLDER
    # Expected one argument "command" all other are separated by | or not
    if step.argument.has_key('command'):
       command = step.argument.get('command')
    else:
       command = step.params.pop(0)
    # add the run folder if specified
    command_arg = '%s %s' %(os.path.join(cfg.bin_folder,command),' '.join(step.params))
    return run_command(cfg,log,step,cfg.runtime_folder,command_arg,True)
#end key_run

def key_ant(cfg,log,step):
    """run one or more ant targets and capture ANT exit code"""
    # detect buildfile parameter
    if step.has_arg('buildfile'):
       build_file=step.get_arg('buildfile')
    elif cfg.has_var('BUILD_FILE'):
       build_file=cfg.get_var('BUILD_FILE')    
    else:
       build_file=r'${BIN_FOLDER}\build.xml'
    # new property_file can be used to set additional ANT properties
    if step.has_arg('property_file'):       
      property_file= step.get_arg('property_file')
    else:
      property_file= os.path.join('${TEST_FOLDER}','build.properties');
    # detect configfile parameter
    if step.has_arg('configfile'):
       config_file=step.get_arg('configfile')
    if step.has_arg('CONFIG_FILE'):
       config_file=step.get_arg('CONFIG_FILE')      
    elif cfg.has_var('CONFIG_FILE'):
       config_file=cfg.get_var('CONFIG_FILE')    
    else:
       raise ValueError('argument not defined: CONFIG_FILE or configfile')
    # detect target
    if step.has_arg('target'):       
       target =step.get_arg('target')
    elif len(step.params)> 0:
       target =' '.join(step.params)
    else:
       raise ValueError('argument not defined: target')
    log.debug('target:%s' % target)
    # predefined ant parameters introduces some pipeline charactersitics to ANT Keyword     
    # note there is an interesting features -k (keep-going) for ant
    output_dir  = os.path.join(cfg.output_folder,step.code)
    # ts_config.createFolder(output_dir)
    TEST_ANT_PARAMS=r"-v -e -f %s -lib ${TEST_HOME}\lib;${TEST_HOME}\pipeline\etc -Dbasedir=${RUNTIME_FOLDER} -Ddir.output=%s -propertyfile %s" 
    ant_params  =TEST_ANT_PARAMS % (build_file, output_dir, property_file)
    ant_params  =cfg.replace_variables(ant_params)
    assert '${' not in ant_params,'not all variables bound: "%s"' % ant_params
    # Builds the commandline
    config_arg  ='-Dconfig.file=%s %s' % (config_file,target)     
    launcher_jar = os.path.join(cfg.ant_home,'lib', 'ant-launcher.jar')
    assert os.path.exists(launcher_jar), 'unable to locate %s' % launcher_jar
    # print cfg.java_home
    command_arg = ('java -classpath %s -Dant.home=%s org.apache.tools.ant.launch.Launcher %s %s' %
                  (launcher_jar, cfg.ant_home, ant_params, config_arg))
    # pipeline ANT will use this environment variable only as information, but will fail if not exist
    os.putenv('TEST_ANT_PARAMS', ant_params)
    return run_command(cfg,log,step,cfg.runtime_folder,command_arg)
#end key_ant

def key_java(cfg,log,step):
    """run class using java runtime"""
    if cfg.has_var('CLASSPATH'):
       command = 'java -classpath %s' % cfg.get_var('CLASSPATH')
    else:   
       command = 'java'
    command_arg = '%s %s' %(command,' '.join(step.params))
    return run_command(cfg,log,step,cfg.runtime_folder,command_arg)
#end key_java

def key_sqlplus(cfg,log,step):
    """run sqlplus script using Oracle client"""
    #expect that login string to be provided else the default login is used
    if step.argument.has_key('login'):
       oracle_login  = step.argument.get('login')
    else:
       raise ValueError('argument not defined: login')
    #expect the script name to be specified as first argument
    if step.argument.has_key('script'):
       script  = step.argument.get('script')
    else:
       script  = step.params.pop(0)
    assert os.path.exists(script), "script file does not exist %s" % script
    if os.path.sep in script:
       runtime_folder = os.path.dirname(script) 
    else:
       runtime_folder = cfg.runtime_folder    
    command_arg    = "sqlplus.exe -S -L %s @%s %s" % (oracle_login,script,' '.join(step.params))    
    command_arg    =  os.path.join(cfg.oracle_home,'bin',command_arg)
    command_arg    =  "echo exit | " + command_arg
    return run_command(cfg,log,step,cfg.runtime_folder,command_arg,True)
#end key_sqlplus


def key_sqlldr(cfg,log,step):
    """load csv file using sqlloader"""
    # expect the profile to be specified or else use normal profile
    if step.argument.has_key('profile'):
       run_profile = step.argument.get('profile')
    else:
       run_profile = 'normal'
    #oracle login can be provided as parameter userid or login
    if step.argument.has_key('userid'):
       login  = step.argument.get('userid')
    else:
       if step.argument.has_key('login'):
          login  = step.argument.get('login')
       else:
          raise ValueError('argument not defined: login')
    assert run_profile in ('normal','fast','turbo'), 'invalid profile "%s". Exprected: normal/fast/turbo}.' % run_profile
    assert len(step.params) == 0, "params not supported. Please provide name=value arguments."
    for element in ('control','data'):
        assert step.argument.has_key(element), "element %s is mandatory" % element
    # convert the arguments into a list of touples
    file_data    = step.argument.get('data')
    file_control = step.argument.get('control')
    #verify files exists
    assert os.path.exists(file_data)   , 'data file does not exist %s' % file_data
    assert os.path.exists(file_control), 'control file does not exist %s' % file_control
    file_name = os.path.split(file_data)[1]
    file_root = file_name[0:file_name.index(".")]
    file_root = os.path.join(cfg.output_folder,file_root)
    # prepare bad file for later check
    if step.argument.has_key('bad'):
       file_bad = step.argument.get('bad')
    else:
       file_bad = file_root+'.bad'
    # map options
    defmt = {}  
    defmt['userid'] = login  
    defmt['data']   = file_data    
    defmt['control']= file_control 
    defmt['bad']    = file_bad     
    defmt['log']    = file_root+'.log'
    defmt['discard']= file_root+'.dis'
    if run_profile in ('fast','turbo'):
       defmt['skip_unusable_indexes'] = 'TRUE'  #disallow/allow unusable indexes or index partitions
       defmt['skip_index_maintenance']= 'TRUE'  #do not maintain indexes, mark affected indexes as unusable
       defmt['direct']                = 'TRUE'  #use direct path       
    if run_profile == 'turbo':
       defmt['direct']        ='TRUE' #use direct path
       defmt['parallel']      ='TRUE' #do parallel load
       defmt['multithreading']='TRUE' #use multithreading in direct path
       
    # create a list of arguments arguments
    arg_list    = ['%s=%s' % (key,value) for key,value in defmt.iteritems()]
    command_arg = '%s %s' % ('sqlldr',' '.join(arg_list))
    retCode     = run_command(cfg,log,step,cfg.runtime_folder,command_arg)
    if os.path.exists(file_bad): 
      return 1      
    else:  
      return retCode
#end key_sqlldr

def key_plsql(cfg,log,step):
    """run plsql procedure for a specific oracle schema"""
    # http://cx-oracle.sourceforge.net/html/cursor.html
    # Procedure parameters must be addressed by Name=Value separated by |
    if step.argument.has_key('login'):
       oracle_login  = step.argument.get('login')
    else:
       raise ValueError('argument not defined: login')
    if step.argument.has_key('procedure'):
       procedure = step.argument.get('procedure')
    else:
       procedure = step.params.pop(0)
    #connect to oracle
    connection =  set_connection(cfg, log, oracle_login)   
    if not connection: 
       log.error('Fail to find connection object')  
       return -1 
    log.debug("procedure:"+procedure)   
    argument, params = ts_config.split_params(step.params)
    # executing a stored procedure
    if cfg.execute:
      log.info('runing please wait ... ')      
      cursor = connection.cursor()
      cursor.callproc("dbms_output.enable",[1000000])
      try:
         cursor.callproc(procedure, params, argument)
         result = 0         
      except (cx_Oracle.DatabaseError, exc):
         error, = exc.args
         log.error("ORA-%s " % error.code)
         log_error(error.message, cfg, step)
         if error.code ==20001:
            result =  1
         else:   
            raise
      finally:   
         log_dbms(cursor, cfg, step)
         cursor.close()
    else:
      result=0
    return result
#end key_plsql

def key_xunit(cfg,log,step):
    """run xunit test function for a specific oracle schema"""
    # Action can be specified as *, that means all XUNITS
    # Connection string must be specified for every line
    if step.argument.has_key('login'):
       oracle_login  = step.argument.get('login')
    else:
       raise ValueError('argument not defined: login')
    log.debug('login  :'+oracle_login)       
    # try to connect to oracle
    connection = set_connection(cfg,log,oracle_login)
    if not connection:
       log.error('Fail to find connection object')
       return -1 
    # executing a xunit.run stored function
    if step.argument.has_key('package'):
       package = step.argument.get('package')       
       log.debug('package:'+package)               
    else:
       package = None 
    if cfg.execute:
        log.info('runing please wait ... ')      
        cursor     = connection.cursor()
        cursor.callproc("dbms_output.enable",[1000000])
        return_val = cursor.var(cx_Oracle.NUMBER)
        if package:
           exec_func  = cursor.callfunc('xunit.run', return_val, [package])
        else:
           exec_func  = cursor.callfunc('xunit.run', return_val)
        result = return_val.getvalue()
        if result > 0:
           log_dbms(cursor,cfg, step)
        cursor.close()
    else:
       result=0    
    return result
#end key_xunit

def key_connect(cfg,log,step):
     """Connect to database and do noting"""
     #First argument LOGIN=...
     if step.argument.has_key('login'):
        oracle_login  = step.argument.get('login')
     else:
        raise ValueError('argument not defined: login')
     # try to connect to oracle
     connection = set_connection(cfg,log,oracle_login)
     if not connection:
        log.error('Fail to find connection object')
        return -1
     else:
        return 0
        
def key_disconnect(cfg,log,step):
    """Disconnect from database"""
    #First argument LOGIN=...
    if step.argument.has_key('login'):
       oracle_login  = step.argument.get('login')
    else:
       raise ValueError('argument not defined: login')
    close_connection(cfg,oracle_login)
    return 0
        
def key_spool(cfg,log,step):
     """create a CSV report from a SQL script"""
     #First argument LOGIN=...
     if step.argument.has_key('login'):
        oracle_login  = step.argument.get('login')
     else:
        raise ValueError('argument not defined: login')
     # try to connect to oracle
     connection = set_connection(cfg,log,oracle_login)
     if not connection:
        log.error('Failed to connect to oracle using "%s"' %  oracle_login)
        return -1
     cursor     = connection.cursor()
     #Second argument FILE=...
     if step.argument.has_key('file'):
       ofile_name = os.path.join(cfg.output_folder,step.argument.get('file'))
     else:
       ofile_name = os.path.join(cfg.output_folder,cfg.test_name+'_'+step.code+'.csv')
     #open file specified as script
     script = step.argument.get('script')
     if not os.path.exists(script):
        raise ValueError('Script file not found: "%s"' % script)
     else:   
        log.debug('Script file:%s' % script)     
        infile = open(script,'r')
     #verify optional arguments    
     if step.argument.has_key('options'):
        spool_options  = step.argument.get('options')
     else:
        spool_options  = ''
     #create the output file for spooling
     log.info('Spool  file:%s' % ofile_name)
     spool_file = open(ofile_name, 'ab')
     csvwriter  = csv.writer(spool_file, dialect=csv.excel, quoting= csv.QUOTE_NONNUMERIC)
     
     sql_str_list = []
     #parse the sql strings up to ; or / then execute
     sql_str = ""     
     lcount = 0
     for row in infile.readlines():
         lcount  =+1   
         new_sql = False         
         line    = row.strip(' \n')
         if len(line)>0:
            if line[0] == '#' or line[0:2]=='--':
               continue      
            if line[-1] in (';','/'):
               row     = row.strip('\n;/')
               new_sql = True
            #replace ${variable} placeholders with attributes then with general variables if any left
            row = step.replace_variables(row)
            row = cfg.replace_variables(row)
            sql_str = sql_str + row
            assert '${' not in row, 'not all variables bound in sql line #%d: "%s" ' % (lcount,row)
         #register SQL in a list
         if new_sql: 
            log.debug('SQL: %s' % sql_str)            
            sql_str_list.append(sql_str)
            sql_str = ""
     #Verify if last SQL is terminated
     assert sql_str == "", "Error in SQL script must be closed using ;"
     #execute each sql from list and spool 
     count_rows = 0     
     if cfg.execute:
        log.info('runing please wait ... ')      
        for sql_str in sql_str_list:
            cursor.execute(sql_str)
            #write top row as header
            if ('header' in spool_options) or ('h' in spool_options):
               header = cursor.description               
               head_row = [ x[0] for x in header]
               csvwriter.writerow(head_row)
            #write rows to output file
            for row_string in cursor:
                #sometimes query return "message" where message is a comma delimited string
                #I split the row using comma separator or else just use the wor_strig as a list
                if len(row_string)==1:
                   row = row_string[0].split(',')                
                else:   
                   row = row_string
                #encode the result as utf8
                csvwriter.writerow(row)
                count_rows += 1
     #execute sql end                
     spool_file.close()
     #remove empty files
     if (count_rows == 0) and cfg.execute:
        os.remove(ofile_name)
        log.warning('No result records, spool file removed.')
     else:
        log.info('Spooled rows: %s', count_rows)
        
     return 0
#end key_spool

# execute a command using the process and wait for results
# function used in all processes that require a subprocess to run
def run_command(cfg,log,step,runtime_folder,command_arg, use_shell=False):
    log_file_name  = ts_loger.get_file_name(cfg,step,'out')
    err_file_name  = ts_loger.get_file_name(cfg,step,'err')    
    log.debug('command:%s' % command_arg)
    log.debug('output :%s' % log_file_name)
    if cfg.execute:
        log.info('runing please wait ... ')      
        # create 2 logers, one for errors, one for output
        out_log  = ts_loger.openLog(log_file_name)
        err_log  = ts_loger.openLog(err_file_name)
        # transfer file names into step object for XML
        step.log_file_name = log_file_name
        step.err_file_name = err_file_name        
        # initial message (will be printed at the bottom in the file)        
        sep_len = max(len(cfg.script_file),len(command_arg)) 
        out_log.writeln('-'*sep_len)
        out_log.writeln('Test case  : %s' % step.code)
        out_log.writeln('Script code: %s' % cfg.test_code)
        out_log.writeln('Script file: %s' % cfg.script_file)
        out_log.writeln('Command    : %s' % command_arg)
        out_log.writeln('Java       : %s' % cfg.java_home)        
        out_log.writeln('-'*sep_len)
        out_log.file.flush
        process = subprocess.Popen(command_arg, cwd=runtime_folder, shell=use_shell, stdout=out_log.file, stderr=err_log.file)
        retCode = process.wait()
        out_log.close()
        err_log.close()
    else:
        retCode = 0     
    return retCode
#end run_command

# This can stop execution before script or suite end.
def key_exit(cfg,log,step):
    """Force exit from test script into parent test script or out"""
    log.warning('Force exit in case: %s' % step.code)
    if cfg.execute:
       for next_case in cfg.iterator: pass
    if not cfg.execute:
       log.warning('Force exit case may cause suites not to be executed correcly!!')
       return -1
    else:
       return 0

# This is a special new key to load configuration parameters into ORACLE
def key_property_load(cfg,log,step):
    #expect that login string to be provided else the default login is used
    if step.argument.has_key('login'):
       oracle_login  = step.argument.get('login')
    else:
       raise ValueError('argument not defined: login')
    connection =  set_connection(cfg, log, oracle_login)   
    if not connection: 
       log.error('Fail to find connection object')  
       return -1 
    if cfg.execute:
      cursor = connection.cursor()    
      for name,value in cfg.variables.iteritems():
        cursor.execute('INSERT INTO TEST_PROPERTY (PROPERTY_NAME, PROPERTY_VALUE) VALUES (:1,:2)', (name,value))
      connection.commit()
    return 0        
       
       
# Available keywords are registered here as dictionary of functions:
registry = { 'include' :None
            ,'log':key_log
            ,'shell':key_shell
            ,'run':key_run
            ,'ant':key_ant
            ,'sqlplus':key_sqlplus
            ,'java':key_java
            ,'xunit':key_xunit
            ,'plsql':key_plsql
            ,'sqlldr':key_sqlldr
            ,'spool':key_spool
            ,'plugin':key_plugin
            ,'connect':key_connect
            ,'disconnect':key_disconnect
            ,'property_load':key_property_load
            ,'exit':key_exit
            }

# end ts_keyword.py
