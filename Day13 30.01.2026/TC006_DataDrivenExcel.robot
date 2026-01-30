*** Settings ***
Library           SeleniumLibrary
Library           DataDriver                    file=testdata.xlsx    sheet_name=Sheet
Test Template     OrangeHRM Login With Excel
Suite Setup       Open OrangeHRM
Suite Teardown    Close OrangeHRM


*** Variables ***
${URL}        https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${BROWSER}    chrome


*** Keywords ***
Open OrangeHRM
    Open Browser                     ${URL}           ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    name=username    timeout=30s

OrangeHRM Login With Excel
    [Arguments]                ${username}                       ${password}
    Sleep                      2s
    Input Text                 name=username                     ${username}
    Input Text                 name=password                     ${password}
    Sleep                      2s
    Capture Page Screenshot
    Click Button               xpath=//button[@type='submit']
    Sleep                      5s
    Capture Page Screenshot

Close OrangeHRM
    Click Element    xpath=//span[@class='oxd-userdropdown-tab']
    Sleep            2s
    Click Link       Logout
    Sleep            3s
    Close Browser


*** Test Cases ***
TC006_DataDrivenExcel.robot
    # Arguments are taken automatically from Excel

