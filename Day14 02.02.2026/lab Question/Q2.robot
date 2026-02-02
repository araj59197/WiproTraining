*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${APP_URL}      https://demoqa.com/automation-practice-form
${BROWSER}      Chrome
${FIRST_NAME}   Aditya
${LAST_NAME}    Raj

*** Test Cases ***
Automate Basic Web Elements Using Selenium
    Open Browser    ${APP_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    0.2s

    Wait Until Element Is Visible    css=#firstName    10s
    Input Text    css=#firstName    ${FIRST_NAME}
    Input Text    css=#lastName     ${LAST_NAME}

    Scroll Element Into View    css=label[for="gender-radio-1"]
    Wait Until Element Is Visible    css=label[for="gender-radio-1"]    10s
    Execute JavaScript    document.querySelector('label[for="gender-radio-1"]').click()

    Scroll Element Into View    css=label[for="hobbies-checkbox-1"]
    Execute JavaScript    document.querySelector('label[for="hobbies-checkbox-1"]').click()

    ${t}=    Get Title
    Run Keyword If    '${t}' != ''    Log To Console    Title is: ${t}

    Close All Browsers
