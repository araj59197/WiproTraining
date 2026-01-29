*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${url}         https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${browser}     chrome
${username}    Admin
${password}    admin123

*** Test Cases ***
TC003_Logging.robot
    Open Browser                     ${url}                                    ${browser}
    Maximize Browser Window
    Wait Until Element Is Visible    xpath=//input[@placeholder='Username']    10s
    Input Text                       xpath=//input[@placeholder='Username']    ${username}
    Input Text                       xpath=//input[@placeholder='Password']    ${password}
    Capture Page Screenshot          beforelogin.png
    Click Button                     xpath=//button[@type='submit']
    Wait Until Location Contains     /dashboard                                15s
    Wait Until Element Is Visible    xpath=//h6[normalize-space()='Dashboard']    15s
    Capture Page Screenshot          afterlogin.png
    Log                              Login Successful - Dashboard Loaded!
    Close Browser