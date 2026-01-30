*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}               https://www.google.com
${BROWSER}           chrome
${EXPECTED_TITLE}    Google

*** Test Cases ***
Question3 - Simple Browser Test Case
    [Documentation]                  This test opens a browser, navigates to a URL, verifies title, captures screenshot and closes browser
    Open Browser                     ${URL}                                                                                                   ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    name=q                                                                                                   timeout=10s
    Verify Page Title                ${EXPECTED_TITLE}
    Capture Page Screenshot          screenshot_question3.png
    Close Browser

*** Keywords ***
Verify Page Title
    [Arguments]         ${expected_title}
    ${actual_title}=    Get Title
    Should Contain      ${actual_title}                         ${expected_title}
    Log                 Page title verified: ${actual_title}
