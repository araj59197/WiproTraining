# TDD Cycle: Red → Green → Refactor
# RED: Write a failing test first (test doesn't pass because function doesn't exist)
# GREEN: Write minimal code to make the test pass
# REFACTOR: Clean up the code while keeping tests passing

def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


import pytest


def test_divide_by_zero_sample():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
