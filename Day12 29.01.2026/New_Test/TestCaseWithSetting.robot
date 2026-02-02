*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Test With All Settings
    [Documentation]    This test demonstrates all test case settings
    [Tags]             smoke                                            regression
    [Setup]            Open Browser                                     https://www.google.com    chrome
    [Timeout]          1 minute
    Title Should Be    Google
    [Teardown]         Close Browser