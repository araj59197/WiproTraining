*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Library           String

Test Teardown     Close Browser

*** Variables ***
${URL}            https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${BROWSER}        chrome

*** Keywords ***
# 1. Custom User Keywords (Requirement 1)

Open Application
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains Element    name=username    timeout=30s

Login Process
    [Arguments]    ${user}    ${pass}
    # Keyword-Driven Reusable Logic (Requirement 2)
    Input Text      name=username    ${user}
    Input Text      name=password    ${pass}
    Click Button    xpath=//button[@type='submit']
    Sleep           3s

Check Outcome
    [Arguments]    ${expected_outcome}
    IF    '${expected_outcome}' == 'success'
        Wait Until Page Contains    Dashboard    timeout=15s
        Log    Successfully logged in to Dashboard
    ELSE
        # Specifically targeting OrangeHRM's error message locator
        Wait Until Element Is Visible    xpath=//div[@role='alert']    timeout=15s
        Element Should Contain    xpath=//div[@role='alert']    Invalid credentials
        Log    Correctly identified invalid credentials error
    END
    Capture Page Screenshot

# 3. Test Template Logic for Data-Driven Testing (Requirement 3)
Run Login Test Case
    [Arguments]    ${u}    ${p}    ${result}
    Open Application
    Login Process    ${u}    ${p}
    Check Outcome    ${result}

*** Test Cases ***
# 2. Keyword-Driven Testing (Requirement 2)
TC1: Standard Keyword-Driven Test
    [Documentation]    Explicitly calls custom keywords for a hardcoded scenario.
    [Tags]    keyword-driven
    Open Application
    Login Process    Admin    admin123
    Check Outcome    success

# 3, 4, 5. Data-Driven Testing using External CSV & Template (Requirement 3, 4, 5)
TC2: Loop-Based Data-Driven Test from CSV
    [Documentation]    Iterates through CSV data rows and executes test logic.
    [Tags]    data-driven
    ${content}=    Get File    ${CURDIR}/login_data.csv
    ${lines}=    Split To Lines    ${content}
    FOR    ${line}    IN    @{lines}
        ${row}=    Split String    ${line}    separator=,
        Log    Executing Data Row: User=${row[0]}, Pass=${row[1]}, Expected=${row[2]}
        # Requirement 5: Pass/fail status for each data row handled by Run Keyword And Continue On Failure
        Run Keyword And Continue On Failure    Run Login Test Case    ${row[0]}    ${row[1]}    ${row[2]}
        Run Keyword And Ignore Error    Close Browser
    END
