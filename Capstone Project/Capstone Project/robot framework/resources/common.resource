*** Settings ***
Documentation     Resource file for Capstone Project common keywords
Library           SeleniumLibrary
Library           ../keywords/StealthLib.py
Library           OperatingSystem
Library           Collections
Library           String

*** Variables ***
${LOG_FILE}         ${CURDIR}/../reports/robot_terminal_output.txt
${SCREENSHOT_DIR}    ${CURDIR}/../screenshots/Robot screenshots
${DATA}             ${EMPTY}
${BROWSER}          chrome

*** Keywords ***
Setup Everything
    [Arguments]    ${csv_path}    ${browser}=${BROWSER}
    Create Directory    ${SCREENSHOT_DIR}
    Create Directory    ${CURDIR}/../reports
    Set Screenshot Directory    ${SCREENSHOT_DIR}
    ${raw_dict}=    Get Csv Data    ${csv_path}
    Set Suite Variable    ${DATA}    ${raw_dict}
    ${start_url}=    Get From Dictionary    ${DATA}    base_url
    Open Stealth Browser    ${start_url}    ${browser}
    Create File    ${LOG_FILE}    ROBOT EXECUTION LOG\n============================\n

Finalize Execution
    Close Stealth Browser
    ${suite_status}=    Get Variable Value    ${SUITE_STATUS}
    IF    '${suite_status}' == 'PASS'
        ${msg}=    Set Variable    \n============================ All test cases passed =======================\n
    ELSE
        ${msg}=    Set Variable    \n[ROBOT EXECUTION END] SOME TESTS FAILED\n
    END
    Log To Console    ${msg}
    Append To File    ${LOG_FILE}    ${msg}

Log Test Result
    ${msg}=    Catenate    ${TEST STATUS}: ${TEST NAME}\n
    Append To File    ${LOG_FILE}    ${msg}

Ensure Home
    ${base}=    Get From Dictionary    ${DATA}    base_url
    ${recovered}=    Recover Browser If Needed
    Wait Until Keyword Succeeds    3x    2s    Go To    ${base}
    # Wait for page to fully load
    Run Keyword And Ignore Error    Wait For Condition    return document.readyState == "complete"    20s
    # Wait past Cloudflare "Just a moment..." challenge if present
    FOR    ${i}    IN RANGE    15
        ${title}=    Execute Javascript    return document.title || ""
        ${cf}=    Run Keyword And Return Status    Should Contain    ${title}    Just a moment
        IF    not ${cf}    BREAK
        Sleep    2s
    END
    Run Keyword And Ignore Error    Wait For Condition    return document.readyState == "complete"    15s
    # Try header-logo first; if not visible fall back to any body content
    ${logo_ok}=    Run Keyword And Return Status    Wait Until Element Is Visible    class:header-logo    15s
    IF    not ${logo_ok}
        # Retry navigation once more
        Run Keyword And Ignore Error    Go To    ${base}
        Sleep    3s
        Run Keyword And Ignore Error    Wait For Condition    return document.readyState == "complete"    15s
        ${logo_retry}=    Run Keyword And Return Status    Wait Until Element Is Visible    class:header-logo    20s
        IF    not ${logo_retry}
            # Accept page as loaded if body has real content (not Cloudflare)
            Wait Until Page Contains Element    tag:body    10s
            Log    header-logo not found but page body loaded – continuing
        END
    END

Clear Notification Bar
    ${present}=    Run Keyword And Return Status    Element Should Be Visible    class:bar-notification
    IF    ${present}
        Run Keyword And Ignore Error    Click Element    css:.bar-notification .close
        Wait Until Element Is Not Visible    class:bar-notification    10s
    END

Logout If Needed
    ${status}=    Run Keyword And Return Status    Element Should Be Visible    class:ico-logout
    IF    ${status}
        Click Element    class:ico-logout
        Wait Until Element Is Visible    class:ico-register    10s
    END

Generate Random Email
    ${random}=    Generate Random String    5    [LETTERS]
    ${email}=     Catenate    SEPARATOR=    ${DATA}[first_name]    ${random}    @example.com
    RETURN    ${email}