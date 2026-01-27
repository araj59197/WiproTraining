# Requirement 1: File named test_*.py (test_calculator.py) with test_ functions
import pytest
from calculator import add, subtract, multiply, divide

# Requirement 3: Use assert statements to validate results
def test_add():
    print("Testing add function...")
    assert add(2, 3) == 5
    print("2 + 3 = 5 ✓")
    assert add(-1, 1) == 0
    print("-1 + 1 = 0 ✓")
    assert add(0, 0) == 0
    print("0 + 0 = 0 ✓")

def test_subtract():
    print("Testing subtract function...")
    assert subtract(10, 5) == 5
    print("10 - 5 = 5 ✓")
    assert subtract(5, 10) == -5
    print("5 - 10 = -5 ✓")

def test_multiply():
    print("Testing multiply function...")
    assert multiply(3, 4) == 12
    print("3 * 4 = 12 ✓")
    assert multiply(5, 0) == 0
    print("5 * 0 = 0 ✓")

def test_divide():
    print("Testing divide function...")
    assert divide(10, 2) == 5.0
    print("10 / 2 = 5.0 ✓")
    assert divide(9, 3) == 3.0
    print("9 / 3 = 3.0 ✓")

# Requirement 4: Test that exception is raised for division by zero
def test_divide_by_zero():
    print("Testing division by zero exception...")
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
    print("ZeroDivisionError raised correctly ✓")
