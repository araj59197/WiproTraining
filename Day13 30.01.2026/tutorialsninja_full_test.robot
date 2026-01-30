*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Library           String
Library           DateTime

Suite Setup       Setup Test Suite
Suite Teardown    Close Browser

*** Variables ***
${URL_REG}        https://tutorialsninja.com/demo/index.php?route=account/register
${URL_LOGIN}      https://tutorialsninja.com/demo/index.php?route=account/login
${BROWSER}        chrome
${REG_DATA}       registration_data.csv
${LOGIN_DATA}     login_data.csv

*** Keywords ***
Setup Test Suite
    [Documentation]    Prepares the test run by cleaning artifacts and opening browser.
    Cleanup Old Screenshots
    Open Browser To Main Page

Cleanup Old Screenshots
    [Documentation]    Deletes old PNG screenshots to ensure a fresh outcome.
    Run Keyword And Ignore Error    Remove File    *.png
    Log    Deleted previous screenshot files.

Open Browser To Main Page
    Open Browser    https://tutorialsninja.com/demo/    ${BROWSER}
    Maximize Browser Window
    Capture Page Screenshot    main_page_loaded.png

Generate Unique Email
    [Arguments]    ${firstname}    ${lastname}
    # Pattern: araj59197@gmail.com (first_initial + lastname + 5_random_digits)
    ${first_initial}=    Get Substring    ${firstname}    0    1
    ${random_num}=       Generate Random String    5    [NUMBERS]
    ${email}=            Set Variable    ${first_initial.lower()}${lastname.lower()}${random_num}@gmail.com
    RETURN    ${email}

Register User
    [Arguments]    ${fname}    ${lname}    ${phone}    ${pwd}    
    Go To    ${URL_REG}
    Wait Until Element Is Visible    id:input-firstname    timeout=15s
    Capture Page Screenshot    register_page_loaded.png
    
    ${email}=    Generate Unique Email    ${fname}    ${lname}
    Log    Registering with Email: ${email}    console=True
    
    Input Text    id:input-firstname    ${fname}
    Input Text    id:input-lastname     ${lname}
    Input Text    id:input-email        ${email}
    Input Text    id:input-telephone    ${phone}
    Input Text    id:input-password     ${pwd}
    Input Text    id:input-confirm      ${pwd}
    
    Capture Page Screenshot    registration_form_filled_${fname}.png

    # Handle subscribe (default to No)
    Execute Javascript    document.querySelector("input[name='newsletter'][value='0']").click()
    
    # Privacy Policy & Submit
    Execute Javascript    document.querySelector("input[name='agree']").click()
    Execute Javascript    document.querySelector("input.btn-primary").click()
    
    # Verification
    Wait Until Page Contains    Your Account Has Been Created!    timeout=10s
    Capture Page Screenshot    registration_success_${fname}.png
    Log    Successfully Registered: ${email}
    
    # Robust Logout
    Go To    https://tutorialsninja.com/demo/index.php?route=account/logout
    Wait Until Page Contains    Account Logout    timeout=10s
    Capture Page Screenshot    logout_success_${fname}.png
    Click Link    Continue
    Wait Until Page Contains    My Account    timeout=10s

Login User
    [Arguments]    ${email}    ${password}    ${expected}
    Go To    ${URL_LOGIN}
    Wait Until Element Is Visible    id:input-email    timeout=20s
    Capture Page Screenshot    login_page_loaded.png
    
    Input Text       id:input-email       ${email}
    Input Text       id:input-password    ${password}
    Capture Page Screenshot    login_form_filled_${email}.png
    Click Button     xpath://input[@value='Login']
    
    Verify Login Outcome    ${email}    ${expected}

Verify Login Outcome
    [Arguments]    ${email}    ${expected}
    IF    '${expected}' == 'success'
        Wait Until Page Contains    My Account    timeout=10s
        Capture Page Screenshot    login_success_${email}.png
        # Logout after success
        Go To    https://tutorialsninja.com/demo/index.php?route=account/logout
    ELSE
        Wait Until Element Is Visible    css:.alert-danger    timeout=10s
        # Check for either the standard error OR the lockout error
        ${alert_text}=    Get Text    css:.alert-danger
        Should Be True    'Warning: No match for E-Mail Address and/or Password.' in '''${alert_text}''' or 'Warning: Your account has exceeded allowed number of login attempts.' in '''${alert_text}'''
        Capture Page Screenshot    login_failure_alert_${email}.png
    END

*** Test Cases ***
TC1: Data-Driven Registration
    [Documentation]    Registers users from CSV data.
    ${csv_content}=    Get File    ${REG_DATA}
    ${lines}=    Split To Lines    ${csv_content}
    
    FOR    ${line}    IN    @{lines}
        Continue For Loop If    'firstname' in '${line}'
        ${data}=    Split String    ${line}    separator=,
        Run Keyword And Continue On Failure    Register User    ${data[0]}    ${data[1]}    ${data[2]}    ${data[3]}
    END

TC2: Data-Driven Login
    [Documentation]    Tests login functionality.
    [Setup]    Go To    ${URL_LOGIN}
    
    ${csv_content}=    Get File    ${LOGIN_DATA}
    ${lines}=    Split To Lines    ${csv_content}
    
    FOR    ${line}    IN    @{lines}
        Continue For Loop If    'email' in '${line}'
        ${data}=    Split String    ${line}    separator=,
        Log    Logging in with: ${data[0]}
        Run Keyword And Continue On Failure    Login User    ${data[0]}    ${data[1]}    ${data[2]}
    END
