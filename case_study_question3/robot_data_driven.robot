*** Settings ***
Library           SeleniumLibrary
Suite Setup       Open Browser       http://127.0.0.1:5002    Chrome
Suite Teardown    Close Browser

*** Variables ***
@{NAMES}       David Lee     Emma Davis     Frank Miller
@{AGES}        35            42             50
@{GENDERS}     Male          Female         Male
@{CONTACTS}    1111111111    2222222222     3333333333
@{DISEASES}    Diabetes      Flu            Migraine
@{DOCTORS}     Dr. Smith     Dr. Johnson    Dr. Williams

*** Test Cases ***
Data Driven Patient Registration
    [Tags]                         data-driven
    FOR                            ${index}                 IN RANGE    3
    Go To                          http://127.0.0.1:5002
    Register Patient Using Data    ${index}
    Go Back
    END

*** Keywords ***
Register Patient Using Data
    [Arguments]                  ${index}
    Input Text                   id=name                           ${NAMES}[${index}]
    Input Text                   id=age                            ${AGES}[${index}]
    ${gender}=                   Set Variable                      ${GENDERS}[${index}]
    Run Keyword If               '${gender}' == 'Male'             Click Element            id=male
    ...                          ELSE                              Click Element            id=female
    Input Text                   id=contact                        ${CONTACTS}[${index}]
    Input Text                   id=disease                        ${DISEASES}[${index}]
    Select From List By Label    id=doctor                         ${DOCTORS}[${index}]
    Click Button                 xpath=//button[@type='submit']
    Sleep                        1s
