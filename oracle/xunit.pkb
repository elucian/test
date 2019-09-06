CREATE OR REPLACE PACKAGE BODY xUNIT IS

  -- predefined conventions
  TEST_INIT     CONSTANT VARCHAR2(10) := 'INIT';
  TEST_TEARDOWN CONSTANT VARCHAR2(10) := 'TEARDOWN';

  -- Internul number of errors
  err_count INTEGER := 0;

  -- Local procedure to read the error log buffers
  PROCEDURE Log2DBMS(i_buff IN VARCHAR2) IS
    g_start_pos INTEGER := 1;
    g_end_pos   INTEGER;
  
    FUNCTION Output_One_Line RETURN BOOLEAN IS
    BEGIN
      g_end_pos := Instr(i_buff, Chr(10), g_start_pos);
    
      CASE g_end_pos > 0
        WHEN TRUE THEN
          DBMS_OUTPUT.PUT_LINE(Substr(i_buff, g_start_pos, g_end_pos - g_start_pos));
          g_start_pos := g_end_pos + 1;
          RETURN TRUE;
        WHEN FALSE THEN
          DBMS_OUTPUT.PUT_LINE(Substr(i_buff, g_start_pos, (Length(i_buff) - g_start_pos) + 1));
          RETURN FALSE;
      END CASE;
    END Output_One_Line;
  
  BEGIN
    WHILE Output_One_Line()
    LOOP
      NULL;
    END LOOP;
  END Log2DBMS;

  -- public procedure to show errors from an exception block
  PROCEDURE log_errors IS
  BEGIN
    Log2DBMS('Error_Stack...' || Chr(10) || DBMS_UTILITY.FORMAT_ERROR_STACK());
    Log2DBMS('Error_Backtrace...' || Chr(10) || DBMS_UTILITY.FORMAT_ERROR_BACKTRACE());
  END log_errors;

  -- boolean assert
  PROCEDURE assert(p_exp BOOLEAN, message VARCHAR2) IS
  BEGIN
    IF NOT p_exp
    THEN
      err_count := err_count + 1;
      raise_application_error(-20001, 'Assert Error:' || message);
    END IF;
  END assert;

  -- return true or false if errors or no errors
  FUNCTION has_errors RETURN BOOLEAN IS
  BEGIN
    RETURN(err_count > 0);
  END has_errors;

  -- format the anonymous pl/sql block to run a pl/sql procedure
  FUNCTION plsql(p_procedure VARCHAR2) RETURN VARCHAR2 IS
    v_block VARCHAR2(250);
  BEGIN
    v_block := 'begin ' || p_procedure || ';' || ' end;';
    RETURN v_block;
  END plsql;

  -- run one single procedure and return 0 if pass or 1 when fail
  FUNCTION run_case(p_unit VARCHAR2) RETURN INTEGER IS
  BEGIN
    EXECUTE IMMEDIATE plsql(p_unit);
    dbms_output.put_line('Pass:' || p_unit);
    RETURN 0;
  EXCEPTION
    WHEN OTHERS THEN
      dbms_output.put_line('Fail:' || p_unit || ',fail');
      log_errors;
      RETURN 1;
  END run_case;

  -- local procedure to run only one single test package
  FUNCTION run_test(p_test_code VARCHAR2) RETURN INTEGER IS
    row_index   INTEGER := 0;
    v_proc_name VARCHAR2(60);
  BEGIN
    -- init and run the current test
    BEGIN
      row_index := 1;
      EXECUTE IMMEDIATE (plsql(p_test_code || '.' || TEST_INIT));
      row_index := 2;
      FOR rec IN (SELECT procedure_name proc_name
                  FROM   user_procedures
                  WHERE  procedure_name LIKE 'CHECK%'
                         AND object_name = p_test_code
                         AND object_type = 'PACKAGE')
      LOOP
        v_proc_name := p_test_code || '.' || rec.proc_name;
        err_count   := err_count + run_case(v_proc_name);
      END LOOP;
      row_index := 3;
      EXECUTE IMMEDIATE (plsql(p_test_code || '.' || TEST_TEARDOWN));
    EXCEPTION
      WHEN OTHERS THEN
        err_count := err_count + 1;
        log_errors;
    END;
    -- teatdown the test
    IF row_index = 2
    THEN
      EXECUTE IMMEDIATE (plsql(p_test_code || '.' || TEST_TEARDOWN));
    END IF;
    RETURN err_count;
  END run_test;

  -- run a test unit or all test units
  FUNCTION run(p_test_package VARCHAR2 := NULL) RETURN INTEGER IS
    -- cursor get the package names when is not null
    CURSOR suites(filter VARCHAR2) IS
      SELECT object_name
      FROM   user_objects
      WHERE  object_type = 'PACKAGE'
             AND object_name LIKE filter;
    filter     VARCHAR2(30);
    fail_count INTEGER := 0;
  BEGIN
    -- verify if package is a test
    assert((p_test_package IS NULL) OR (p_test_package LIKE 'TEST_%') OR (p_test_package LIKE 'test_%')
          ,'Package name must be like "TEST_*"');
    -- support for null package name
    IF p_test_package IS NULL
    THEN
      filter := 'TEST_%';
    ELSE
      filter := p_test_package;
    END IF;
    -- scan all test packages
    FOR rec IN suites(filter)
    LOOP
      fail_count := fail_count + run_test(rec.object_name);
      IF fail_count = 0
      THEN
        dbms_output.put_line('Test ' || rec.object_name || ' pass');
      ELSE
        dbms_output.put_line('Test ' || rec.object_name || ' fail');
      END IF;
    END LOOP;
    RETURN fail_count;
  END run;

END xUNIT;
/
