*** Settings ***
Documentation    Pipe separated format example
Library          SeleniumLibrary

*** Variables ***
${URL}    https://www.google.com

*** Test Cases ***
Pipe Format Test
    Open Browser       ${URL}    chrome
    Title Should Be    Google
    Close Browser
