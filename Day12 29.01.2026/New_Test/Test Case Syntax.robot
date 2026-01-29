*** Settings ***
Library    SeleniumLibrary

*** Keywords ***
Open Login Page
    Open Browser               https://practicetestautomation.com/practice-test-login/    chrome
    Maximize Browser Window

Input Username
    [Arguments]    ${username}
    Input Text     id=username    ${username}

Input Password
    [Arguments]    ${password}
    Input Text     id=password    ${password}

Submit Credentials
    Click Button    id=submit

Welcome Page Should Be Open
    Wait Until Page Contains    Congratulations    10s

Error Message Should Be Visible
    Wait Until Page Contains    Your username is invalid!    10s

*** Test Cases ***
Valid Login
    [Documentation]                Tests valid user login
    [Tags]                         smoke                     login
    Open Login Page
    Input Username                 student
    Input Password                 Password123
    Submit Credentials
    Welcome Page Should Be Open
    Close Browser

Invalid Login
    [Documentation]                    Tests invalid login
    [Tags]                             negative
    Open Login Page
    Input Username                     invalid
    Input Password                     wrong
    Submit Credentials
    Error Message Should Be Visible
    Close Browser