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
    Click Button                     xpath=//button[@type='submit']
    Sleep                            5s
    Location Should Contain          /dashboard
    Log                              Login Successful - Dashboard Loaded!
    Close Browser