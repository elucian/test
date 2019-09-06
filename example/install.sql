-- Create table
@@hello.prc


create table SAMPLE
(
  ID   NUMBER(10),
  NAME VARCHAR2(20)
);
/

create or replace package test_sample is

  -- Author  : EMOISE
  -- Created : 7/20/2011 9:04:12 AM
  -- Purpose : Sample xUNIT test
  
  -- Public function and procedure declarations
  procedure init;
  procedure teardown;
  
  procedure check_sample0;
  procedure check_sample1;
  procedure check_sample2;

end test_sample;
/

create or replace package body test_sample is

  procedure init is
  begin
    dbms_output.put_line('Init was run');
  end init;  
  
  procedure teardown is
  begin
    dbms_output.put_line('Teardown was run');
  end teardown;  

  procedure check_sample0 is
  begin
    xunit.assert(1=1, 'this is a positive test, 1=1');
  end;  

  
  procedure check_sample1 is
  begin
    xunit.assert(1=3, 'this is a negative test, 1!=3');
  end;  
  
  procedure check_sample2 is
  begin
    xunit.assert(1=2, 'this is a negative test, 1!=2');    
  end;    

end test_sample;
/