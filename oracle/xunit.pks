CREATE OR REPLACE PACKAGE xUNIT IS
  /**
  *Utility for pipeline PL/SQL unit testing
  */

  -- public exception assert_error
  assert_error EXCEPTION;
  PRAGMA EXCEPTION_INIT(assert_error, -20001);

  /** verify an assumption expression
  * @param p_exp Boolean value or expression to be check
  * @param message The exception message if p_exp is false
  * @throws assert_error ORA: 20001 with message
  */
  PROCEDURE assert(p_exp BOOLEAN, message VARCHAR2);

  /* verify error state for last run */
  FUNCTION has_errors RETURN BOOLEAN;

  /* show the error messages to dbms_output */
  PROCEDURE log_errors;

  /**
  * This is the procedure used to execute one or all unit test packages
  * @param p_test_package = package name to run or null for all packages
  * @return number of errors
  */
  FUNCTION run(p_test_package VARCHAR2 := NULL) RETURN INTEGER;

END xUNIT;
/
