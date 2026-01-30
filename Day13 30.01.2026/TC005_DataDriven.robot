*** Settings ***
Test Template    Login Test
Library          SeleniumLibrary

*** Variables ***
${url}        https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${browser}    chrome

*** Keywords ***
Login Test
    [Arguments]                      ${url}                       ${browser}     ${username}    ${password}
    Open Browser                     ${url}                       ${browser}
    Maximize Browser Window
    Wait Until Element Is Visible    //input[@name='username']    timeout=10s
    Input Text                       //input[@name='username']    ${username}
    Input Text                       //input[@name='password']    ${password}
    Click Element                    //button[@type='submit']
    Sleep                            3s
    Capture Page Screenshot          login_screenshot.png
    Close Browser

*** Test Cases ***
Valid Login With Admin Credentials
    ${url}    ${browser}    Admin    admin123


