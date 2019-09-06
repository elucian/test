## Define work-flow

A workflow is procedure that can resolve a large problem. We organize work in small steps that have meaning and can be executed one by one until the end of the procedure. Steps may pass or fail and developer can make decisions what to do in each situation.

## Define Step
A _step_ is an executable _"region"_ that can contain one or several statements. It has a name and a description. The sequence of steps create a workflow. The workflow ends with {recover|finalize} or the end of section. 

## Work-flow syntax
```
method <name>()
  .description="procedure description";  
resolve
  job <step_name>("describe the step"): 
    <step_implementation>;
    when <step_condition> then [pass | fail | skip | raise | return];
  job <step_name>():
    <step_implementation>;
    [when <step_condition> then raise(code,"error message");]
    ...
  [recover]
    <exception_region>
  [finalize]
    <output_report>;
method <name>;
```

## Step structure
The \<step_name> can be a normal identifier. It can be as simple as {a1,a2,a3} or {case1, case2} or  {step_10,step_20}. It is a good practice to use \<prefix>_nnn pattern. We can count the steps at interval of 10 or 100 so that steps can be reorganized. You can count from 10 to 10 like 110...990. So you have space to insert other steps.

## Step description
The \<description> of the step is of type string. Description of the step is stored in a local collection that is a list of executed steps[]. This local structure can be used for introspection after the workflow was executed. 

# Current step 
The current step is identified using keyword  _step_ and can be used with dot operator. For example current step description is: step.description; This variable is available in recovery section and in the step section. We can create exception handlers using current step status and name. We can create step references using notation "@Step".

```
recover
  use step
    print(name);
    print(description);
    print(status);
  use;
```

### Early termination
In the step region programmer can make decisions to verify if the step has pass or has failed. The execution of steps can be interrupted and resumed. The _"resume"_ keyword will continue execution of steps with the next step. The _return_ will continue execution with finalization region.

```
when <condition> then [ pass | fail | skip | raise | panic | return ];

if <condition> then 
   pass | fail | skip | raise | panic | return ;
end if;
```
* pass; : continue with next statement
* fail; : continue with next statement
* skip; : skip over next step and continue with one after it if there is one
* skip <step_name> : skip forward to <step_name>;
* return; : stop sequences of steps and execute finalization region
* raise(code,"message"); : stop sequences of steps and execute recovery region

**Note:** It is not possible to return to one of previous steps using a skip. 

### Step status
A step can have status: {fail, pass, error, none} 
* default status is "none"
* pass;  : record status= pass
* fail;  : record status= fail
* raise; : record status= error
* panic; : record status= fail

Using these clauses developer can record status in workflow report. If an exception is raised during one step then execution of next step is interrupted. Program continue with recover region, finalization region then return execution to the caller. 

### Workflow Trace
Any workflow has a variable _"trace"_ predefined. This variable is a collection of records that can be used to display workflow status. This variable can be used in the finalization region to display the report or save content into a file. 

```
  trace: Array(n) of Step;
```
### Workflow library
We define Step record type in standard _runner_ library:

```
-- This is a fragment declaration from workflow library
...
type Step: Record (
  name: String,        {*name of the step *}
  status: String,      {*pass/fail/error/none*}
  description: String, {*step description*}
  start_date: Date,    {*the start date*}
  start_time: Time,    {*the start time*}
  end_time: Time,      {*the end time*}
  err_message: String, {*exception message*} 
  err_code: String     {*exception code*} 
);
```

### How to use workflow?

```
#type:runner

import 
  from workflow use Step;

procedure test_workflow():
  v:Integer;
execute
  this.description="procedure test_workflow description ";
  v=5;
step:a
  when v<5 then pass; 
step:b
  when v>5 then fail;
step:c
  when v==5 then return; 
step:d
  pass; --> this will never execute
recover
  if step.name in ["a","b"] then
     resume;
  else
     fail;
  end if;
finalize
  -- display error trace to console 
  let
    i,err:Integer;
    st:Step;
  loop
    when i>trace.length then stop;
    st=trace[i];
    print('step #s has #s' <-(st.name,st.status))
    if st.status in ["fail","error"] then
       err+=1;             
    end if;
    i+=1;
  loop; 
  if err > 0 then
     print("workflow #s has #d errors" <- (this.name, err));
  else
     print("workflow #s is successful" <- this.name);
  end if; 
procedure;
```
This is the trace report:
```
step a has pass;  
step b has fail; 
step c has stop; 
workflow test_workflow has 1 errors
```
#### What to do with the workflow _trace_ report?
A trace can be used to create a report file or record the report into a database or generate a web page. Whatever the business  requires. Developers can create beautiful HTML reports using templates or can even create xml reports for test automation. 

Each module has it''s own trace report. We can have a common trace report define in main program even if the main program is not using steps. If a global variable $trace is defined the module trace report can be appended to global report.

**Example:**
```
-- This is a program that demonstrate workflow
#work_trace:all
#work_echo:off

import;
  from runner use Step, Trace;

variable 
  $trace: Trace;

-- This is a local workflow
procedure work(p:Integer):
execute
  this.description="simple workflow";
step:s1
  print("p^2=" & p^2);
step:s2
  print("p^3=" & p^3);
finalize
  $trace.append(trace);
procedure;

-- main program
procedure main:
execute
  work(2);
  work(3);
finalize
  $trace.save;
procedure;
```

## Workflow directives
A workflow is usually a module of type:aspect. Usually the program that coordinate execution of workflows is called "aspect". Also a "driver" can call workflow execution. 

* #trace:err|all|off  -- create trace records for ...errors, all or none
* #echo:on|off        -- each step print out to console when is executed
* #log:on|off         -- each workflow create an automatic log file when is running
* #auto:off|on        -- when error if found in a step we record and continue with next step

**Note:** First value is the default.

## Workflow usability
Workflows can be used to create test cases for large processes. One program can have hundreds of workflows organized in modules. A program can use jobs to run the workflows in parallel. This is a simple solution to create a multi-thread application and improve performance.

Workflows can be used to log-out information about the processes. Each run of workflow can record important information about the step performance and status. This log can be visualized while the program is running on the console or file. 