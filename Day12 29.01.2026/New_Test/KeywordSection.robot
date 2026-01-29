*** Keywords ***
Open Login Page
    Open Browser               https://example.com/login    chrome
    Maximize Browser Window

Input Username
    [Arguments]    ${username}
    Input Text     id=username    ${username}

Input Password
    [Arguments]    ${password}
    Input Text     id=password    ${password}

Submit Credentials
    Click Button    id=login-button

Login With Credentials
    [Arguments]           ${user}                           ${pass}
    [Documentation]       Logs in with given credentials
    Input Username        ${user}
    Input Password        ${pass}
    Submit Credentials