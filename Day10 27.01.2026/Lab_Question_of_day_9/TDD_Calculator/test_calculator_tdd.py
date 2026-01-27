import pytest
from calculator_tdd import add, subtract, multiply, divide


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(5, 10) == -5


def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(3, 0) == 0


def test_divide():
    assert divide(10, 2) == 5
    assert divide(5, 2) == 2.5


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
