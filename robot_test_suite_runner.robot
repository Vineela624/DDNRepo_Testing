*** Settings ***
Documentation     Runs the entire Python Unittest suite (test_suite.py) 
...               as a single Robot Framework test case.
Library           OperatingSystem

*** Variables ***
${PYTHON_TEST_COMMAND}    python test_suite.py

*** Test Cases ***
Execute Python Unittest Suite
    [Documentation]    Executes test_suite.py and verifies all 8 internal tests passed.
    [Tags]    Python    Unittest    Suite_Runner
    Run And Verify The Python Unittest Suite

*** Keywords ***
Run And Verify The Python Unittest Suite
    [Documentation]    Executes the external Python unittest file and confirms it passes (returns exit code 0).

    Log To Console    \n--- Executing Python Unittest Suite (${PYTHON_TEST_COMMAND}) ---\n
    
    # Run the Python script. If any unittest within test_suite.py fails, 
    # the script will return a non-zero exit code (typically 1), causing 
    # Robot's 'Run' keyword to fail the test.
    ${output}=    Run    ${PYTHON_TEST_COMMAND}
    
    Log To Console    \n--- Python Script Output ---\n
    Log To Console    ${output}
    
    # Verify that the summary line indicating all tests ran successfully is present.
    Should Contain    ${output}    Ran 8 tests in 
    Should Contain    ${output}    OK
    Log To Console    \n--- Python Suite Execution Successful ---
