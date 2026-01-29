*** Settings ***
Library          SeleniumLibrary
Test Template    Login Test
Test Setup       Open Browser       https://practicetestautomation.com/practice-test-login/    chrome
Test Teardown    Close Browser

*** Test Cases ***
Valid Login      student    Password123
Invalid Login    user       wrongpass

*** Keywords ***
Login Test
    [Arguments]     ${username}    ${password}
    Input Text      id=username    ${username}
    Input Text      id=password    ${password}
    Click Button    id=submit
