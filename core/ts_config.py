#######################################################
# pra_config configuration package for PTA
#######################################################
import platform
import os
import re
import copy
import getpass
import shlex
import uuid
import csv
from datetime import datetime

g_build_number = None
g_artifact_location = None

def set_build_number(b_number):
    global g_build_number
    g_build_number=b_number   

def set_artifact_loc(p_location):
    global g_artifact_location
    g_artifact_location=p_location  
    
# prepare the predefined variable values
def get_time_strig():
    s_time        = datetime.now()
    return 'M{month:0>2}D{day:0>2}-H{hour:0>2}M{min:0>2}S{sec:0>2}'.format(month=s_time.month,day=s_time.day,hour=s_time.hour,min=s_time.minute,sec=s_time.second)

def vdecor(p_variable):
    """Decorate a predefined variable"""
    return '${'+p_variable+'}'

def ant_decor(p_variable):
    """Decorate a predefined variable for ant"""
    return '@{'+p_variable+'}'

def get_boolean(p_string):
    return p_string in ('true','TRUE','True','yes','YES','Yes')

def strip_quotes(p_str):
  if len(p_str)>0  and p_str[0]=='"' and p_str[-1]=='"' and p_str.count('"')==2:
     return p_str.strip('"')
  else:
     return p_str

     
# Parse the template and store into a list of touples
# return list of dic containing values for each row
def parse_loop_config(loop_config):    
  file = open(loop_config, 'rb') 
  loop_list  = []  
  try:
    reader   = csv.reader(file)
    var_list = reader.next()
    #prepare dictionary for one row
    for var_values in reader:  
        row_dic = {}
        for i in range(len(var_list)):
            row_dic[var_list[i].strip()]=var_values[i].strip();      
        loop_list.append(row_dic)
    return loop_list
  finally:
    file.close()
    
# A test case can be a script (not parsed) or a command call
# The argument is split into a list and dictionary of values
# Arguments can contain variable placeholders ${}, prepared in next_case() function
class case_object:    
    """enclapsulate a test case"""
    def __init__(self,p_code,p_path,arg_list,p_when_pass,p_when_fail,p_severity):
        pattern   = '[a-zA-Z0-9_]'
        fix_code  = ''.join(re.findall(pattern, p_code))
        assert p_code==fix_code, 'Invalid caracter in test case code:"%s"' % p_code 
        self.code        = p_code
        self.path        = p_path
        self.argument    = dict(arg_list)
        if self.argument.has_key('keyword'):
           self.keyword = self.argument.pop('keyword')
        else:
           raise ValueError('keyword argument not specified for case "%s"' % p_code)
        if self.argument.has_key('description'):
           self.description = self.argument.pop('description')
        else:
           self.description = ""
        if self.argument.has_key('params'):
           value  = self.argument.pop('params')
           patern = re.compile(r'\s*=\s*')  #prepare spaces
           value  = patern.sub('=',value)   #remove spaces 
           #shlex.whitespace_split = True
           self.params = shlex.split(value,posix=True) #preserve quoted strings
        else:
           self.params = []
        # read status for case: enable/disable
        if self.argument.has_key('status'):
           self.status = self.argument.pop('status')
        else:
           self.status = "skip"
        # read or create optional properties when_pass
        if self.argument.has_key('when_pass'):
           self.when_pass = self.argument.pop('when_pass')
        else:
           self.when_pass = p_when_pass        
        # read or create optional properties when_fail 
        if self.argument.has_key('when_fail'):
           self.when_fail = self.argument.pop('when_fail')
        else:
           self.when_fail = p_when_fail
        # read or create optional severity
        if self.argument.has_key('severity'):
           self.severity = self.argument.pop('severity')
        else:
           self.severity = p_severity
           assert self.severity in ('minor','major')
        # read the loop configuration
        self.next_loop = 0
        if self.argument.has_key('loop_config'):
           self.loop_config = self.argument.get('loop_config')
           self.loop_list   = []
        # default properties
        self.start_time  = datetime.now()
        self.end_time    = datetime.now()
        self.duration    = datetime.now() - datetime.now()
        # logs are recorded after key execution
        self.log_file_name = None
        self.err_file_name = None
    def get_arg(self, variable_name):
        if self.has_arg(variable_name):
           return self.argument.get(variable_name)
        else:
           raise ValueError('Argument not found "%s"' % variable_name)
    def has_arg(self, variable_name):
        return self.argument.has_key(variable_name)
    # verify if all variables are prepared
    def check_prepared(self):
        for key,value in self.argument.iteritems():
            if '${' in value: raise ValueError('Variable not defined in %s=%s ' % (key,value))
        for value in self.params:
            if '${' in value: raise ValueError('Variable not defined in "params" :%s' % value)
    #when we start, and never finish is an error
    def start_case(self):
        self.start_time  = datetime.now()
        self.status      = 'start'
    #if we manage to finish, we will record pass or fail message
    def end_case(self,status):
        self.end_time = datetime.now()
        self.duration = self.end_time - self.start_time
        #non fatal errors are ignored
        if status in ['fail','critical','error'] and self.severity=='minor':
           self.status   = 'ignore'
        else:  
           self.status   = status
    #this function will transfer arguments from loop_config into case arguments
    #when the loop is ended the next_loop will be -1 < 0
    def set_loop_args(self):
        current_loop=self.next_loop
        self.next_loop += 1
        if current_loop<len(self.loop_list):
           self.argument = copy.deepcopy(self.argument_backup)
           self.params   = copy.deepcopy(self.params_backup)
           new_argument_dic=self.loop_list[current_loop]
           self.argument.update(new_argument_dic)
        else:
           self.next_loop=-1
    #this function parse loop configuration file and reset next_loop  to 0
    def start_loop(self):
        self.loop_list = parse_loop_config(self.loop_config)
        #self.loop_list  = parse_loop_config(self.loop_config)
        self.next_loop = 0
        self.argument_backup = copy.deepcopy(self.argument)
        self.params_backup   = copy.deepcopy(self.params)
    #this function enumerate arguments and replace placeholders with arguments
    def refresh_arguments(self):
        for okey, ovalue in self.argument.iteritems():
            for ikey, ivalue in self.argument.iteritems():
                idecor = vdecor(ikey)
                if idecor in ovalue:
                   self.argument[okey]=ovalue.replace(idecor,ivalue)
    #this function enumerate parameter and replace placeholders with arguments                   
    def refresh_parameters(self):
        for i in range(len(self.params)):
            for key, value in self.argument.iteritems():
                decor = vdecor(key)
                if decor in self.params[i]:
                   self.params[i]=self.params[i].replace(decor,value)          
    #this function use argument values to replace variables into a string
    def replace_variables(self, p_value):
        v_value = p_value
        for r_name, r_value in self.argument.iteritems():
            v_value = v_value.replace(vdecor(r_name),r_value)
        return v_value
#end class case_object

# The configuration will read configuration file into properties
# All cases are stored as a list named: test_cases of case_objects
# Parent configuration and parent case (p_config, p_case) are optional
class config_parser:
    def __init__(self,script_file,config_param,parent_config=None,parent_case=None):
        #predefined variable values
        oracle_home     = os.getenv('ORACLE_HOME', None)
        TEST_home   = os.getenv('TEST_HOME', None)
        ant_home        = os.getenv('ANT_HOME', None)
        java_home       = os.getenv('JAVA_HOME', None)
        
        
        assert oracle_home    ,'Missing environment variable ORACLE_HOME'  
        assert TEST_home  ,'Missing environment variable TEST_HOME'
        assert ant_home       ,'Missing environment variable ANT_HOME'
        
        self.oracle_home     = os.path.normpath(oracle_home)     
        self.TEST_home   = os.path.normpath(TEST_home)
        self.ant_home        = os.path.normpath(ant_home)
        self.java_home       = os.path.normpath(java_home)
        self.start_time      = get_time_strig()

        #establish a name
        self.script_file = os.path.normpath(script_file)
        self.script_name = script_file.split(os.path.sep)[-1]
        self.test_name   = self.script_name.partition('.')[0]
        self.test_type   = self.script_name.partition('.')[2]
        assert self.test_type in ('script','suite'), 'Unrecognized script file extension. Expected "script" or "suite"'

        # establish the test code
        if parent_case:
           # is a script or a suite of suites
           self.test_code = parent_case.code
           self.path      = parent_case.path+'.'+self.test_code
           self.severity  = parent_case.severity
        else:
           # is a primary test suite
           self.test_code = self.test_name
           self.path      = self.test_code
           self.severity  = 'major'
           
        # default values, later overvriten in config parser
        self.description = self.script_name
        self.when_pass  = 'next'
        self.when_fail  = 'exit'

        #default main action
        self.execute = False

        # create variable dictionary
        if parent_config:
           # inherit uppercased variables from parent
           self.variables={}
           for key,value in parent_config.variables.iteritems():
              if key==key.upper(): self.variables[key]=value
        else:
           # predefined inheritable variables
           self.variables={'ORACLE_HOME'  :self.oracle_home,
                           'TEST_HOME':self.TEST_home,
                           'ANT_HOME'     :self.TEST_home,
                           'START_TIME'   :self.start_time,
                           'NODE_NAME'    :platform.node(),
                           'USER_NAME'    :getpass.getuser(),
                           'JAVA_HOME'    :self.java_home
                          }
           # overwrite the default user name if -u parameter is used
           if config_param != 'unspecified':
                self.variables['CONFIG_PARAM'] = config_param
           else:      
                self.variables['CONFIG_PARAM'] = self.variables['USER_NAME']
                
           # store build number as predefined variable
           if g_build_number:
                self.variables['BUILD_NUMBER'] = g_build_number
           else:
                self.variables['BUILD_NUMBER'] = str(uuid.uuid1())
                           
           if g_artifact_location:               
                self.variables['ARTIFACT_LOCATION'] = g_artifact_location
           else:
                self.variables['ARTIFACT_LOCATION'] = ""                
                           
        # overvrite variables related to test configuration
        # we need the new value for these variables
        self.variables['TEST_NAME']   = self.test_name
        self.variables['TEST_CODE']   = self.test_code
        self.variables['SCRIPT_NAME'] = self.script_name

        # use parameters from parent include statement
        # only uppercase arguments are used
        if parent_case:
           for key, value in parent_case.argument.iteritems():
               if key==key.upper(): self.variables[key]=value

        # eventual read inherited ANT configuration
        if self.variables.has_key('CONFIG_FILE'):
           self.parse_config_file()

        # two important colections will be extracted from parse_script
        self.test_cases   = {}  #this comes from "case:" category in the script (case_code:case_object)
        self.test_list    = []  #this comes from "workflow:" ordered list of scripts to be executed
        self.parse_script(self.script_file)

        # prepare iterator for function next_case
        # Note: I have changed iterator in last version
        self.iterator = self.test_list.__iter__()

        #establish the runtime folder
        self.runtime_folder=self.get_var('RUNTIME_FOLDER');
        self.bin_folder    =self.get_var('BIN_FOLDER');
         
        #enhanced output folder  
        if parent_config: 
           self.output_folder = os.path.join(parent_config.output_folder,self.test_code)                
        else:
           self.output_folder = self.get_var('OUTPUT_FOLDER')
    #end __init__

    # parse the script file and store variables
    def parse_script(self, script_file):
        assert os.path.exists(script_file), 'Script file not found: " %s"' %script_file

        # open script file for read only
        script = open(script_file,'r')

        # initial values for parser
        indent   = False     # first line is not indented, but we face identation for test_name and description
        line     = 0         # current line number
        arg_list = []        # arguments is a list of touples (name, value)
        arg_dic  = {}        # dictionary is unique and we need this for checking syntax
        sections  = ['test', 'option', 'variable', 'case','end']
        # optional category: 'default','private','public'
        if self.test_type == 'suite':
           mandatory = ['test', 'variable','case','end']
        else:
           mandatory = ['test','case','end']
        # prepare first iteration
        current_category  = None      # category not yet defined
        current_value     = None      # category value not yet defined
        previous_category = None      # category not yet defined
        previous_value    = None      # category value not yet defined
        # scan all lines in the file
        for item in script:
            line +=1
            pure  = item.strip()
            # ignore empty lines and comments
            if pure =='' or pure[0]=='#':
               continue
            # Verify and close previous category
            if not indent and previous_category:
               self.close_category(previous_category,previous_value,arg_list, arg_dic)
               arg_list = [] # new list, is reused to define the workflow or case arguments
               arg_dic  = {} # dictionary is not used, so elements are lost
            # verify line syntax
            if item[0] == ' ':
               indent = True
               words  = pure.partition('=')
               arg    = words[0].strip()
               val    = words[2].strip()
               assert item[0:2] =='  ', 'Please use at least 2 spaces for indentation in line %s.' % (line)
               assert arg not in [arg_dic], 'Duplicated argument "%s" in line %d.' % (arg,line)
               arg_list.append((arg,val))
               arg_dic[arg]=val
            else:
               # next category
               indent = False
               if ':' in pure:
                  if '=' in pure and pure.index(':') > pure.index('='):
                      raise ValueError('Incorect syntax in script "%s" line %d expected ":", but "=" found in col:%d' % (self.script_name,line,pure.index('=')))
               else:
                  raise ValueError('Incorect syntax in script "%s" line %d expected ":"' % (self.script_name,line))
               words = pure.partition(':')
               category   = words[0].strip()
               value      = words[2].strip()
               # verify next category
               if category not in sections:
                  raise ValueError('Unexpected category in script "%s": "%s" in line %d' % (self.script_name,category,line))
               if category in mandatory:
                  mandatory.remove(category)
               if category!='case':
                  sections.remove(category)
               # prepare next iteration
               previous_category  = current_category
               previous_value     = current_value
               current_category   = category
               current_value      = value
        #end for
        self.close_category(previous_category,previous_value,arg_list, arg_dic)
        self.close_category(category,value,arg_list,arg_dic)
        assert len(mandatory)   == 0, 'Undefined category detected: [%s]' %  ','.join(mandatory)
    #end def parse_script

    # close one category at a time
    def close_category(self,category,value,arg_list, arg_dic):
       # preconditions
       if category in ['test','end']:
          assert(value==self.test_name),'Expected test name = "%s" in script "%s"' % (self.test_name,self.script_name)
       # detect category test (test suite or test script)
       if  category == 'test':
           self.description = arg_dic['description']
           if 'when_pass' in arg_dic: self.when_pass   = arg_dic['when_pass']
           if 'when_fail' in arg_dic: self.when_fail   = arg_dic['when_fail']
           if 'severity'  in arg_dic: self.severity    = arg_dic['severity']
       elif category=='case':
          if value in self.test_cases:
             raise ValueError('Duplicate case not allowed in script "%s", case: "%s"' % (self.script_name,value))
          else:
             self.test_cases[value]=case_object(value,self.path,arg_list,self.when_pass,self.when_fail,self.severity)
          self.test_list.append(value)
       elif category == 'variable':
          # create user variables and update variable dictionary
          # if variable already exists, the old value is preserved
          for v_name, v_value in arg_list:
               v_value = self.replace_variables(v_value)
               if '_FILE' in v_value or '_FOLDER' in v_value:
                  v_value = os.path.normpath(v_value)
               if not self.variables.has_key(v_name):
                  self.variables[v_name]=v_value
                  if v_name=='CONFIG_FILE':self.parse_config_file()
       elif category == 'end':
          pass
       else:
          raise ValueError('Unrecognized category "%s" in script "%s"' % (category,self.script_name))
    # end close_category

    # Modify execution flag
    def set_execute(self,main_action,next_action):
        if main_action == 'execute':
          self.execute= (next_action=='continue')
        elif main_action == 'resume':
           self.execute= (next_action in ['next','break','resume'])
        elif main_action == 'debug':
           self.execute= (next_action in ['next','resume','break'])
        else:
           self.execute=False

    #Parse ant CONFIG file and compute variable substitution
    def parse_config_file(self):
        #check if config file is specified
        config_file = self.get_var('CONFIG_FILE')
        file = open(config_file)
        var_list = []
        for item in file.readlines():
            # find position of first blank character or '=' in row
            item = item.strip()
            if item=='' or item[0]=='#':
               continue
            assert (' ' in item or '=' in item), 'Invalid ant config format in line: "%s"' % item
            if '=' in item:
               pos = item.index('=')
            else:
               pos = item.index(' ')
            var   = item[0:pos].strip()
            value = item[pos:].strip()
            if value[0] == '=':
               value = value[1:].strip()
            # replace placeholders ${var} with previous properties
            for key,val in var_list:
                value = value.replace(vdecor(key),val)
                for key, val in self.variables.iteritems():
                    value = value.replace(vdecor(key),val)
                    value = value.replace(vdecor(key.lower()),val)
            var_list.append((var,value))
        # variables are updated with new properties
        self.variables.update(var_list)
    #end parse_config_file

    #check if a variable is defined
    def has_var(self,var_name):
        return self.variables.has_key(var_name)

    # return a user variable if defined otherwise return None
    def get_var(self,var_name):
        if self.variables.has_key(var_name):
           return self.variables.get(var_name)
        else:
           raise ValueError('variable %r not found' % var_name)

    #update internal variables to new values
    #before update the value is replaced with internal variables to remove ${} placeholders
    def update_var(self, var_dic):
        for key,val in var_dic.iteritems():        
            full_val = self.replace_variables(val)
            self.variables.update({key:full_val})

    #replace the occurance of ${variable} in parameter with values
    def replace_variables(self, p_value):
        v_value = p_value
        for r_name, r_value in self.variables.iteritems():
            v_value = v_value.replace(vdecor(r_name),r_value)
        return v_value

    #based on notation @variable=value modify an configuration variable
    #the variable is permanently modified into one configuration space
    #the configuration variable may exits or may do not exist
    #this procedure is called for each case execution in ts_driver
    def update_var_case(self, case):
       for key,value in case.argument.iteritems():
           if key[0]=='@':
              self.update_var({key[1:]:value})
        
    #minimalistic check the exit/breack code is valid
    #code can have a dot when is part of a script
    #code can have a + when regular expresions are used to match
    #code can be == '*' when user wish to debug everithing
    def check_code(self, p_code):
        if p_code:
            if '+' in p_code: return
            if '.' in p_code:
               script_name  =  p_code.split('.',1)[0]
               if script_name not in self.test_cases:
                  raise NameError('Script not found: "%s"' % script_name)
            else:
               if p_code not in self.test_cases:
                  raise NameError('Case not found: "%s"' % p_code)
    #end has_code

    #Oracle connections pool dictionary, every connection is identified by "login" key
    #Connections is maintained during a test suite execution until is closed
    connections = {}

#end class config_parser

# Function split_argument will split a list of elements into a dictionary and a list
def split_params(p_list):
        """ parse a script record or argument and return a dictionary and a list"""
        argument  = {}
        params    = []
        for element in p_list:
            element = element.strip()
            if len(element)==0: continue
            if (element[0]!='"') and  ('=' in element):
               word = element.partition('=')
               name = word[0].strip()
               value= word[2].strip()
               argument[name] = value
            else:
               params.append(element)
        return argument, params

def createFolder(folder):
    """ recursive create the folders requested """
    if not os.path.exists(folder):
       os.makedirs(folder)
    if not os.path.exists(folder):
       raise OSError("Can't create folder " + folder)
#end createFolder

def checkFolders(cfg):
    """ verify if all the folders are in place """
    # create output folder
    createFolder(cfg.output_folder)
    # verify output folder
    assert os.listdir(cfg.output_folder) == [], 'Error: Output folder not empty!' 
    # check mandatory folders
    for key, val in cfg.variables.iteritems():
        if  key in {'ORACLE_HOME','TEST_HOME','ANT_HOME','OUTPUT_FOLDER','SCRIPT_FOLDER','RUNTIME_FOLDER','BIN_FOLDER'} and not os.path.exists(val):
            raise ValueError('Mandatory folder does not exist: %s=%s' %  (key, val))
        if  ('${' not in val) and (key[-7:] == '.config' or key[-5:] =='.file' or key[-4:] =='.dir' ) and ('/' in val or '\\' in val) and not os.path.exists(val):
            raise ValueError('File or folder does not exist: %s=%s' %  (key, val))
        if  (key[-7:] == '_FOLDER') and (cfg.get_var('OUTPUT_FOLDER') in val):
            createFolder(val)
            
#end checkFolder
