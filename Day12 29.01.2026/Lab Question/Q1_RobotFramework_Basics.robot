*** Settings ***
Library          BuiltIn
Library          Collections
Documentation    Robot Framework Basics - Demonstrating variables, logging, and test cases

*** Variables ***
# Scalar Variables
${NAME}       John Doe
${AGE}        30
${CITY}       New York
${MESSAGE}    Hello from Robot Framework!

# List Variables
@{FRUITS}     Apple    Banana    Orange    Mango    Grapes
@{NUMBERS}    1        2         3         4        5

*** Test Cases ***
Test Case 1 - Scalar Variables and Logging
    [Documentation]    This test demonstrates the use of scalar variables and logging
    [Tags]             basics                                                            logging

    Log               Starting Test Case 1
    Log To Console    \n========================================
    Log To Console    Test Case 1: Scalar Variables and Logging
    Log To Console    ========================================

    # Log scalar variables
    Log               Name: ${NAME}
    Log               Age: ${AGE}
    Log               City: ${CITY}
    Log To Console    Name: ${NAME}
    Log To Console    Age: ${AGE}
    Log To Console    City: ${CITY}

    # Log a message variable
    Log               ${MESSAGE}
    Log To Console    ${MESSAGE}

    # Verify values
    Should Be Equal               ${NAME}    John Doe
    Should Be Equal As Numbers    ${AGE}     30

    Log To Console    \nTest Case 1 Completed Successfully!

Test Case 2 - List Variables and Iteration
    [Documentation]    This test demonstrates the use of list variables
    [Tags]             basics                                              list

    Log               Starting Test Case 2
    Log To Console    \n========================================
    Log To Console    Test Case 2: List Variables and Iteration
    Log To Console    ========================================

    # Log list variables
    Log Many    @{FRUITS}
    Log Many    @{NUMBERS}

    # Display list length
    ${fruit_count}=    Get Length                      ${FRUITS}
    Log                Total Fruits: ${fruit_count}
    Log To Console     Total Fruits: ${fruit_count}

    # Access list items by index
    Log               First Fruit: ${FRUITS}[0]
    Log               Second Fruit: ${FRUITS}[1]
    Log To Console    First Fruit: ${FRUITS}[0]
    Log To Console    Second Fruit: ${FRUITS}[1]

    # Loop through list items
    Log To Console    \nAll Fruits:
    FOR               ${fruit}           IN    @{FRUITS}
    Log               Fruit: ${fruit}
    Log To Console    - ${fruit}
    END

    # Loop through numbers
    Log To Console    \nAll Numbers:
    FOR               ${num}            IN    @{NUMBERS}
    Log               Number: ${num}
    Log To Console    - ${num}
    END

    Log To Console    \nTest Case 2 Completed Successfully!

Test Case 3 - Variable Operations
    [Documentation]    This test demonstrates variable operations and string concatenation
    [Tags]             basics                                                                 operations

    Log To Console    \n========================================
    Log To Console    Test Case 3: Variable Operations
    Log To Console    ========================================

    # String concatenation
    ${full_message}=    Set Variable                     ${MESSAGE} Welcome ${NAME}!
    Log                 ${full_message}
    Log To Console      Full Message: ${full_message}

    # Mathematical operations
    ${sum}=           Evaluate                      ${AGE} + 10
    ${product}=       Evaluate                      ${AGE} * 2
    Log               Age after 10 years: ${sum}
    Log               Double the age: ${product}
    Log To Console    Age after 10 years: ${sum}
    Log To Console    Double the age: ${product}

    # Working with list operations
    ${first_three_fruits}=    Get Slice From List                        ${FRUITS}                0    3
    Log Many                  First 3 Fruits:                            @{first_three_fruits}
    Log To Console            \nFirst 3 Fruits: ${first_three_fruits}

    Log To Console    \nTest Case 3 Completed Successfully!

Test Case 4 - Conditional Logic
    [Documentation]    This test demonstrates conditional statements
    [Tags]             basics                                           conditionals

    Log To Console    \n========================================
    Log To Console    Test Case 4: Conditional Logic
    Log To Console    ========================================

    # IF condition with age
    IF                ${AGE} >= 18
    Log               ${NAME} is an adult
    Log To Console    ${NAME} is an adult (Age: ${AGE})
    ELSE
    Log               ${NAME} is a minor
    Log To Console    ${NAME} is a minor (Age: ${AGE})
    END

    # Check if item exists in list
    ${item}=          Set Variable                        Apple
    IF                '${item}' in @{FRUITS}
    Log               ${item} found in fruits list
    Log To Console    ${item} found in fruits list
    ELSE
    Log               ${item} not found in fruits list
    Log To Console    ${item} not found in fruits list
    END
