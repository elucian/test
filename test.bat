@ECHO OFF
REM Script used to call the pipeline test suites

SET  NLS_LANG=.AL32UTF8

if "%TEST_HOME%"==""  (
   ECHO Environment variable TEST_HOME not defined
   SET  TEST_HOME=%~dp0%\pipeline
)


if "%ANT_HOME%"=="" (
   ECHO Environment variable ANT_HOME not defined
   EXIT /b 1
)

if "%ORACLE_HOME%"==""  (
   ECHO Environment variable ORACLE_HOME not defined
   EXIT /b 1
)


python.exe %TEST_HOME%\main.py %*

if "%errorlevel%"=="0" (
   echo Test suite succesful
) else (
   echo Test suite failed
   EXIT /b 1
)