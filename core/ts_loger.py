import logging
import os

# log levels
#   logging.DEBUG
#   logging.INFO,
#   logging.WARNING
#   logging.ERROR
#   logging.CRITICAL}

log_level = logging.DEBUG


# Standard Python Loger will display messages to console & log into file
# is using several log level and messages all the time starts with :INFO, DEBUG, ERROR or WARNING
def setupLog(cfg, main_action):
   global log_level 
   if main_action in ['debug','check']:
       log_level= logging.DEBUG
   else:   
       log_level= logging.INFO

   logging.basicConfig(format='%(levelname)s: %(message)s',level=log_level)
  
   # create a file loger on demand    
   log_file_name = cfg.get_var('LOG_FILE')
      
   result  = logging.getLogger(log_file_name)
   result.raiseException=True      
   # Establish the log record format
   if log_level == logging.DEBUG:
      str_format = '%(asctime)-15s %(levelname)-8s %(module)-12s #%(lineno)03d %(message)s'
   else:
      str_format = '%(asctime)-15s %(levelname)-8s %(message)s'
   # Crete file handler
   fileHandler   = logging.FileHandler(log_file_name, mode='a', encoding=None, delay=False)     
   fileHandler.setFormatter(logging.Formatter(fmt=str_format))
   result.addHandler(fileHandler)  
   # Check if log is created
   if not os.path.exists(log_file_name):  
      raise OSError("Can't create log file " + log_file_name)
   return result

# conventional log file, useful for record plain outputs 
class openLog:
    # raw text, based on simple text outputs
    # output file name must be specified
    def __init__(self,file_name):
      self.file_name = file_name
      out_file = open(file_name,'w+')
      self.file = out_file
       
    # write one word
    def write(self,str):
       self.file.write(str)
       
    # write one line   
    def writeln(self,str=None):
       if str: self.file.write(str)
       self.file.write('\n')
       
    # write many lines at once
    def writelines(self,lst):
        new_list = {element+'\n' for element in lst}
        self.file.writelines(new_list)
    # close the writer    
    def close(self):
       self.file.seek(0)
       line = self.file.readline()
       self.file.close()
       if len(line) == 0:
          os.remove(self.file_name)

# convention: the output folder is the {OUTPUT_FOLDER}/test_code/step_code
# the folder is created if does not exist, the file is not oppened
def get_file_name(cfg,step,ext):
    file_path_name = os.path.join(cfg.output_folder,'%s.%s' % (step.code,ext))
    return file_path_name 

#end      