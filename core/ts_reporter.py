import csv

class mem_report:
    """define memory structure for a report"""
    def __init__(self,cfg):
        self.description   = cfg.description
        self.TEST_home = cfg.get_var('TEST_HOME')
        self.test_name     = cfg.get_var('TEST_NAME')        
        self.file_name     = cfg.get_var('REPORT_FILE')
        self.output_folder = cfg.get_var('OUTPUT_FOLDER')
        self.artifact_url  = cfg.get_var('ARTIFACT_LOCATION')
        if cfg.has_var('XML_FILE'):  
           self.xml_file_name = cfg.get_var('XML_FILE')
        self.test_header   = ["Parent Script","Test Case","Keyword","Description","Start_Time","Duration(s)","Result","out_file_name","err_file_name"]

    #end init 

    def convert_to_url(self, p_full_file_name):
        if self.artifact_url:
          result = p_full_file_name.replace(self.TEST_home, "");            
          result = self.artifact_url + "artifact/" + result + "/*view*/"
          result = result.replace('/\\','/').replace('\\','/')
          return result
        else:
          return p_full_file_name
    
    # create report file
    def start(self):
        #create CSV file
        self.report_file   = open(self.file_name,'wb+')
        self.writer        = csv.writer(self.report_file   , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.writer.writerow(self.test_header)

    # Write a test script result in report file
    def csv_row(self,step):
        duration='{:.3f}'.format((step.duration.seconds*1000+step.duration.microseconds/1000.0)/1000)
        #Write to CSV one row 
        self.writer.writerow([
           step.path
          ,step.code
          ,step.keyword
          ,step.description
          ,step.start_time.strftime("%I:%M:%S %p")
          ,duration
          ,step.status
          ,step.log_file_name
          ,step.err_file_name
        ])
    
    # Empty the memory buffer to disk
    def flush_file(self):      
        self.report_file.flush()     

    # Finalize the report      
    def close(self):
        self.report_file.close()           

    def build_xml(self,tests,failures,time):
        #create xml file
        xml       = open(self.xml_file_name,'wb')
        xml.write('<testsuites name="%s" tests="%s" failures="%s" time="%s">\r' % (self.test_name,tests,failures,time))
        cases = csv.reader(open(self.file_name, "rb"))
        fields = cases.next()
        prev_script = '_' 
        #Write in XML file
        for row in sorted(cases):
            case_script    = row[0]
            case_name      = row[1]
            case_type      = row[2]
            case_desc      = row[3]
            case_start     = row[4]
            case_time      = row[5]
            case_status    = row[6]
            log_file_name  = row[7]
            err_file_name  = row[8]
            if (prev_script != case_script):
                if (prev_script != '_'):
                    #close previous element
                    xml.write('</testsuite>\r')
                prev_script = case_script
                #new testsuite element
                xml.write('<testsuite name="%s">\r'% prev_script)
            #new tescase element with properties 
            xml.write('<testcase name="%s" time="%s" status="%s">' % (case_name,case_time,case_status))
            if case_status in ['fail','critical']:
               xml.write('<failure type="pta.%s"/>' % case_type)
            elif case_status in ['error','ignore']:
               xml.write('<error/>')
            elif case_status in ['skip','disable']:
               xml.write('<skipped/>')
            #close the test-case element
            if log_file_name:
                  xml.write('\r<system-out>')
                  xml.write(self.convert_to_url(log_file_name))
                  xml.write('</system-out>\r')
            if err_file_name:
                  xml.write('\r<system-err>')
                  xml.write(self.convert_to_url(err_file_name))
                  xml.write('</system-err>\r')           
            #Closing test case element
            xml.write('</testcase>\r')
        #close last element
        xml.write('</testsuite>\r')            
        #close XML
        xml.write('</testsuites>\r')
        xml.close()

#end mem_report
