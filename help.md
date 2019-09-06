## Command Line

You can run test suites ussing command:
-----------------------------------------
If we use BNF notation here is the full syntax:

As a remainder for BNF:

[] = Optional element
|  = One or other
\<> = element name

test.bat \<test_suite> [-a | --action check|execute|debug|resume] [-b | --break \<break_code>] [ -u | --user \<user_name>]  [-n | --number \<build_number>]


New parameter: -l %BUILD_URL%
---------------------------------------------------------------------------------------------
This parameter is used for jenkins to communicate the URL location of artifact. With this we can have a mouse click open output file in case of an error.

<test_suite>
---------------------------------------------------------------------------------------------
Suite name 

<break_code>
---------------------------------------------------------------------------------------------
Using brec option user can establish a break point. 
Break can be used in combination with any other main action.

-b | --break <break_code>

## Examples:
---------------------------------------------------------------------------------------------
1) test.bat test.suite
2) test.bat test.suite -a execute
3) test.bat test.suite -a check
4) test.bat test.suite -a debug
5) test.bat test.suite -a debug  -b IndiaNQ_Jaipur
6) test.bat test.suite -a resume -b IndiaNQ_Jaipur.split

## Check Mode
---------------------------------------------------------------------------------------------
Users can activate check mode using action = "check"
In check mode the workflow is simulated, the command is not executed
Check mode is very fast and useful to find configuration issues.

## Debug Mode
---------------------------------------------------------------------------------------------
User can activate the debug mode by specify -a debug
In debug mode when an error is encontered, the application stops.
      
**Step By Step**

Using action debug and a breack point, application will stop 
in the break point and ask user for next action.

User will specify a next action for every test case.

The following next actions are available in step by step mode: 

a) skip  : current case will not be executed
b) next  : current case will be executed step by step
c) break : user can specify next breack point 
d) resume: script will continue to the end if no breack is matching
e) exit  : execution is terminated immediatle and script fail

Steps to create a new suite
---------------------------------------------------------------------------------------------
1. Copy sample.suite, and sample.cfg  (location is depending if test is private or public)
2. Modify test suite and test script to reflect your workflow
3. Check the scripts using command:
  run_test.bat <test_suite> -a check
4. Run test using command:
  run_test.bat <test_suite> -a execute
5. Investigate the output folder for log files and reports
Log files and report file are created in output folder, 
    names are specified in configuration file.     

## Activity
---------------------------------------------------------------------------------------------
Developer will create test suites, test scripts and python plugins or new keywords.

Tester will create configuration files, will run test suites and will investigate reports
