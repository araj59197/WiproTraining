*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Variables ***
${URL}        http://127.0.0.1:5002
${BROWSER}    Chrome
${DELAY}      2

*** Test Cases ***
Patient Registration - Valid Data
    [Tags]                         smoke
    Open Browser And Navigate
    Sleep                          2s
    Input Patient Details          Alice Johnson    28    Female    9876543210    Asthma    Dr. Smith
    Sleep                          2s
    Submit Form
    Sleep                          2s
    Verify Registration Success    Alice Johnson
    Sleep                          2s
    [Teardown]                     Close Browser

Patient Registration - Multiple Patients
    [Tags]                       regression
    Open Browser And Navigate
    Sleep                        2s
    Input Patient Details        Bob Williams     55    Male    9876543211    Heart Disease    Dr. Johnson
    Sleep                        2s
    Submit Form
    Sleep                        2s
    Go To                        ${URL}
    Sleep                        2s
    Input Patient Details        Charlie Brown    40    Male    9876543212    Arthritis        Dr. Williams
    Sleep                        2s
    Submit Form
    Sleep                        2s
    [Teardown]                   Close Browser

Verify Form Fields
    [Tags]                         smoke
    Open Browser And Navigate
    Sleep                          2s
    Page Should Contain Element    id=name
    Page Should Contain Element    id=age
    Page Should Contain Element    id=male
    Page Should Contain Element    id=female
    Page Should Contain Element    id=contact
    Page Should Contain Element    id=disease
    Page Should Contain Element    id=doctor
    Sleep                          2s
    [Teardown]                     Close Browser

View Patients List
    [Tags]                         smoke
    Open Browser                   ${URL}/patients        ${BROWSER}
    Maximize Browser Window
    Sleep                          2s
    Wait Until Page Contains       Registered Patients
    Page Should Contain Element    id=patientsTable
    ${row_count}=                  Get Element Count      xpath=//tr[@class='patient-row']
    Should Be True                 ${row_count} > 0
    Sleep                          2s
    [Teardown]                     Close Browser

*** Keywords ***
Open Browser And Navigate
    Open Browser                ${URL}                  ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Patient Registration
    Sleep                       1s

Input Patient Details
    [Arguments]                  ${name}                  ${age}                 ${gender}    ${contact}    ${disease}    ${doctor}
    Input Text                   id=name                  ${name}
    Sleep                        0.5s
    Input Text                   id=age                   ${age}
    Sleep                        0.5s
    Run Keyword If               '${gender}' == 'Male'    Select Radio Button    gender       Male
    ...                          ELSE                     Select Radio Button    gender       Female
    Sleep                        0.5s
    Input Text                   id=contact               ${contact}
    Sleep                        0.5s
    Input Text                   id=disease               ${disease}
    Sleep                        0.5s
    Select From List By Label    id=doctor                ${doctor}
    Sleep                        0.5s

Submit Form
    Click Button    xpath=//button[@type='submit']
    Sleep           ${DELAY}

Verify Registration Success
    [Arguments]                 ${expected_name}
    Wait Until Page Contains    Registration Successful
    Page Should Contain         ${expected_name}
