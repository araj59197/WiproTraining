*** Settings ***
Documentation     Demo suite: Suite/Test Setup & Teardown + tags + CLI execution
Suite Setup       Suite Setup Keyword
Suite Teardown    Suite Teardown Keyword
Test Setup        Test Setup Keyword
Test Teardown     Test Teardown Keyword

*** Test Cases ***
Smoke Test - Open Example
    [Tags]    smoke    ui
    Log    This is a SMOKE test case.
    Should Be Equal    2    2

Regression Test - Simple Validation
    [Tags]    regression
    Log    This is a REGRESSION test case.
    Should Contain    Robot Framework    Robot

*** Keywords ***
Suite Setup Keyword
    Log To Console    \n=== SUITE SETUP: Starting test suite ===
    Log               Suite setup executed.

Suite Teardown Keyword
    Log To Console    \n=== SUITE TEARDOWN: Finishing test suite ===
    Log               Suite teardown executed.

Test Setup Keyword
    Log To Console    \n--- TEST SETUP: Before each test ---
    Log               Test setup executed.

Test Teardown Keyword
    Log To Console    \n--- TEST TEARDOWN: After each test ---
    Log               Test teardown executed.
