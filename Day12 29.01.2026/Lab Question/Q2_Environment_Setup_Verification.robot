*** Settings ***
Library          BuiltIn
Library          OperatingSystem
Library          Process
Library          SeleniumLibrary
Library          String
Documentation    Environment Setup Verification - Validates Python, Robot Framework, and SeleniumLibrary

*** Test Cases ***
Test Case 1 - Verify Python Installation
    [Documentation]    Verifies that Python is installed and accessible
    [Tags]             setup                                               python

    Log To Console    \n========================================
    Log To Console    Verifying Python Installation
    Log To Console    ========================================

    TRY
        # Run Python version command
    ${result}=        Run Process                                python    --version    shell=True
    Log               Python command output: ${result.stdout}
    Log To Console    Python Status: ${result.stdout}

        # Check if command was successful
    Should Be Equal As Numbers    ${result.rc}                                  0    
    ...                           msg=Python is not installed or not in PATH

        # Verify Python is accessible
    Should Contain    ${result.stdout}                                     Python
    ...               msg=Python command did not return expected output

    Log               Python is installed and working correctly
    Log To Console    Python is installed and working correctly

    EXCEPT            AS                                                                ${error}
    Log               Python Installation Check FAILED: ${error}                        level=ERROR
    Log To Console    Python Installation Check FAILED
    Log To Console    Error: ${error}
    Log To Console    \nPlease install Python from https://www.python.org/downloads/
    Fail              Python is not properly installed: ${error}
    END

Test Case 2 - Verify Robot Framework Installation
    [Documentation]    Verifies that Robot Framework is installed
    [Tags]             setup                                         robotframework

    Log To Console    \n========================================
    Log To Console    Verifying Robot Framework Installation
    Log To Console    ========================================

    TRY
        # Run robot version command (output goes to stderr on Windows)
    ${result}=    Run Process    robot    --version    shell=True

        # Robot --version outputs to stderr, not stdout
    ${output}=        Set Variable If                              '${result.stderr}' != '${EMPTY}'    ${result.stderr}    ${result.stdout}
    Log               Robot Framework command output: ${output}
    Log To Console    ${output}

        # Verify output contains Robot Framework
    Should Contain    ${output}                                        Robot Framework
    ...               msg=Robot Framework is not properly installed

        # Extract version line
    ${version_line}=    Get Line                                    ${output}    0
    Log                 Robot Framework Version: ${version_line}
    Log To Console      Robot Framework: ${version_line}

    Log               Robot Framework is installed and working correctly
    Log To Console    Robot Framework is installed and working correctly

    EXCEPT            AS                                                              ${error}
    Log               Robot Framework Installation Check FAILED: ${error}             level=ERROR
    Log To Console    Robot Framework Installation Check FAILED
    Log To Console    Error: ${error}
    Log To Console    \nPlease install Robot Framework: pip install robotframework
    Fail              Robot Framework is not properly installed: ${error}
    END

Test Case 3 - Verify SeleniumLibrary Import
    [Documentation]    Verifies that SeleniumLibrary can be imported successfully
    [Tags]             setup                                                         selenium

    Log To Console    \n========================================
    Log To Console    Verifying SeleniumLibrary
    Log To Console    ========================================

    TRY
        # SeleniumLibrary is already imported in Settings section
        # Get library version using Python
    ${result}=    Run Process                                                                        python    -c    
    ...           import SeleniumLibrary; print(f'SeleniumLibrary {SeleniumLibrary.__version__}')
    ...           shell=True

    Log               SeleniumLibrary check output: ${result.stdout}
    Log To Console    ${result.stdout}

        # Check if command was successful
    Should Be Equal As Numbers    ${result.rc}                            0
    ...                           msg=SeleniumLibrary is not installed

        # Verify SeleniumLibrary was imported in Settings
    ${library_status}=    Set Variable         SeleniumLibrary imported successfully
    Log                   ${library_status}
    Log To Console        ${library_status}

        # Test a basic SeleniumLibrary keyword
    ${timeout}=       Get Selenium Timeout
    Log               Selenium Default Timeout: ${timeout}
    Log To Console    Selenium Default Timeout: ${timeout}

    Log               SeleniumLibrary is working correctly
    Log To Console    SeleniumLibrary is working correctly

    EXCEPT            AS                                                                              ${error}
    Log               SeleniumLibrary Check FAILED: ${error}                                          level=ERROR
    Log To Console    SeleniumLibrary Check FAILED
    Log To Console    Error: ${error}
    Log To Console    \nPlease install SeleniumLibrary: pip install robotframework-seleniumlibrary
    Fail              SeleniumLibrary is not properly installed: ${error}
    END

Test Case 4 - Print Robot Framework Version Details
    [Documentation]    Displays detailed Robot Framework version information
    [Tags]             setup                                                    version

    Log To Console    \n========================================
    Log To Console    Robot Framework Version Details
    Log To Console    ========================================

    TRY
        # Get Robot Framework version (from stderr on Windows)
    ${result}=        Run Process        robot                               --version           shell=True
    ${rf_version}=    Set Variable If    '${result.stderr}' != '${EMPTY}'    ${result.stderr}    ${result.stdout}

    Log               Full version output:\n${rf_version}
    Log To Console    \n${rf_version}

        # Get Python version again for complete info
    ${python_result}=    Run Process                  python    --version    shell=True
    Log To Console       \n${python_result.stdout}

        # Get pip list for installed packages
    ${pip_result}=    Run Process                                        pip    list    |    findstr    robot    shell=True
    Log               Installed Robot packages:\n${pip_result.stdout}
    Log To Console    \nInstalled Robot Framework packages:
    Log To Console    ${pip_result.stdout}

    Log               Version information retrieved successfully
    Log To Console    \nVersion information retrieved successfully

    EXCEPT            AS                                                  ${error}
    Log               Could not retrieve all version details: ${error}    level=WARN
    Log To Console    Could not retrieve all version details
    Log To Console    Error: ${error}
        # Don't fail, just warn
    END

Test Case 5 - Comprehensive Environment Check
    [Documentation]    Performs a comprehensive check of all dependencies
    [Tags]             setup                                                 comprehensive

    Log To Console    \n========================================
    Log To Console    Comprehensive Environment Check
    Log To Console    ========================================

    ${all_checks_passed}=    Set Variable    ${True}

    # Check 1: Python
    TRY
    ${result}=                    Run Process     python      --version    shell=True
    Should Be Equal As Numbers    ${result.rc}    0
    Log To Console                Python: PASS
    EXCEPT
    Log To Console                Python: FAIL
    ${all_checks_passed}=         Set Variable    ${False}
    END

    # Check 2: Robot Framework
    TRY
    ${result}=               Run Process              robot                               --version           shell=True
    ${output}=               Set Variable If          '${result.stderr}' != '${EMPTY}'    ${result.stderr}    ${result.stdout}
    Should Contain           ${output}                Robot Framework
    Log To Console           Robot Framework: PASS
    EXCEPT
    Log To Console           Robot Framework: FAIL
    ${all_checks_passed}=    Set Variable             ${False}
    END

    # Check 3: SeleniumLibrary
    TRY
    ${result}=                    Run Process              python      -c    import SeleniumLibrary    shell=True
    Should Be Equal As Numbers    ${result.rc}             0
    Log To Console                SeleniumLibrary: PASS
    EXCEPT
    Log To Console                SeleniumLibrary: FAIL
    ${all_checks_passed}=         Set Variable             ${False}
    END

    # Check 4: pip
    TRY
    ${result}=                    Run Process     pip         --version    shell=True
    Should Be Equal As Numbers    ${result.rc}    0
    Log To Console                pip: PASS
    EXCEPT
    Log To Console                pip: FAIL
    ${all_checks_passed}=         Set Variable    ${False}
    END

    # Final Result
    Log To Console    \n========================================
    IF                ${all_checks_passed}
    Log               ALL ENVIRONMENT CHECKS PASSED
    Log To Console    ALL ENVIRONMENT CHECKS PASSED
    Log To Console    Environment is properly configured!
    ELSE
    Log               SOME ENVIRONMENT CHECKS FAILED                                     level=ERROR
    Log To Console    SOME ENVIRONMENT CHECKS FAILED
    Log To Console    Please review the errors above and install missing dependencies
    Fail              Environment setup is incomplete
    END
    Log To Console    ========================================
