*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${API_URL}    http://127.0.0.1:5000

*** Test Cases ***
verify Get_users
    Create Session                 mysession                  ${API_URL}
    ${response}=                   GET On Session             mysession     /users
    Should Be Equal As Integers    ${response.status_code}    200
    Log To Console                 ${response.json()}

verify Get_user_by_id
    Create Session                 mysession                  ${API_URL}
    ${response}=                   GET On Session             mysession     /users/1
    Should Be Equal As Integers    ${response.status_code}    200
    Log To Console                 ${response.json()}

verify Get_user_not_found
    Create Session                 mysession                  ${API_URL}
    ${response}=                   GET On Session             mysession     /users/999    expected_status=404
    Should Be Equal As Integers    ${response.status_code}    404
    Log To Console                 ${response.json()}

verify Create_user
    Create Session                 mysession                  ${API_URL}
    ${user_data}=                  Create Dictionary          name=Hemant Singh
    ${response}=                   POST On Session            mysession            /users    json=${user_data}
    Should Be Equal As Integers    ${response.status_code}    201
    Log To Console                 ${response.json()}

verify Update_user
    Create Session                 mysession                  ${API_URL}
    ${updated_data}=               Create Dictionary          name=Aditya Kumar
    ${response}=                   PUT On Session             mysession            /users/1    json=${updated_data}
    Should Be Equal As Integers    ${response.status_code}    200
    Log To Console                 ${response.json()}

verify update_partial_user
    Create Session                 mysession                  ${API_URL}
    ${partial_data}=               Create Dictionary          name=Aditya Singh
    ${response}=                   PATCH On Session           mysession            /users/2    json=${partial_data}
    Should Be Equal As Integers    ${response.status_code}    200
    Log To Console                 ${response.json()}

verify Delete_user
    Create Session                 mysession                    ${API_URL}
    ${response}=                   DELETE On Session            mysession     /users/3
    Should Be Equal As Integers    ${response.status_code}      204
    Log To Console                 User deleted successfully