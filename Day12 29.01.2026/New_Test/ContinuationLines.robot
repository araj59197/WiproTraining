*** Settings ***
Documentation    This is a very long documentation string
...              that spans multiple lines for better
...              readability in the test file.

*** Variables ***
${LONG_STRING}    This is a very long string that needs
...               to be split across multiple lines
...               for better readability.

@{LONG_LIST}    item1    item2    item3
...             item4    item5    item6

*** Test Cases ***
Test With Continuation
    Log Many    arg1    arg2    arg3
    ...         arg4    arg5    arg6