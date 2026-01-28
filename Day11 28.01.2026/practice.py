import pytest
import sys


# ==========================================
# 1. ASSERT STATEMENTS AND EXCEPTIONS
# ==========================================


# Simple assert
def test_addition():
    assert 2 + 3 == 5


# Assert with message
def test_subtraction():
    assert 5 - 3 == 2, "Subtraction result is incorrect"


# Function to test exception
def divide(a, b):
    return a / b


# Exception handling with pytest.raises
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


# Exception with message matching
def test_exception_message():
    with pytest.raises(ValueError, match="invalid literal"):
        int("not_a_number")


# ==========================================
# 2. PYTEST MARKERS - SKIP AND XFAIL
# ==========================================


# Skip test unconditionally
@pytest.mark.skip(reason="Feature not implemented yet")
def test_payment():
    assert True


# Conditional skip based on platform
@pytest.mark.skipif(sys.platform != "win32", reason="Windows only test")
def test_windows_feature():
    assert True


# Conditional skip based on Python version
@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_python310_feature():
    assert True


# Expected failure (xfail)
@pytest.mark.xfail(reason="Known bug - ticket #123")
def test_known_issue():
    assert 2 * 2 == 5


# Expected failure that passes (XPASS)
@pytest.mark.xfail(reason="Might pass after fix")
def test_might_pass():
    assert 2 * 2 == 4


# ==========================================
# 3. CUSTOM MARKERS (smoke, regression)
# ==========================================


@pytest.mark.smoke
def test_login_smoke():
    assert True


@pytest.mark.smoke
def test_homepage_smoke():
    assert True


@pytest.mark.regression
def test_user_registration():
    assert True


@pytest.mark.regression
def test_password_reset():
    assert True


# ==========================================
# 4. UNIT TESTS - Calculator Example
# ==========================================


# Calculator functions
def multiply(a, b):
    return a * b


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


# Unit tests
def test_multiply():
    assert multiply(3, 4) == 12


def test_multiply_negative():
    assert multiply(-2, 5) == -10


def test_multiply_zero():
    assert multiply(100, 0) == 0


def test_add():
    assert add(10, 20) == 30


def test_subtract():
    assert subtract(50, 30) == 20


# ==========================================
# 5. FUNCTIONAL TESTS - Auth Example
# ==========================================


# Authentication function
def login(username, password):
    if username == "admin" and password == "admin123":
        return "Login Successful"
    return "Invalid Credentials"


def test_valid_login():
    assert login("admin", "admin123") == "Login Successful"


def test_invalid_login():
    assert login("user", "wrong") == "Invalid Credentials"


def test_empty_credentials():
    assert login("", "") == "Invalid Credentials"


def test_wrong_password():
    assert login("admin", "wrongpass") == "Invalid Credentials"


# ==========================================
# 6. PARAMETERIZED TESTS
# ==========================================


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),
        (0, 5, 0),
        (-1, 4, -4),
        (10, 10, 100),
    ],
)
def test_multiply_parametrized(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    "username, password, expected",
    [
        ("admin", "admin123", "Login Successful"),
        ("admin", "wrong", "Invalid Credentials"),
        ("user", "admin123", "Invalid Credentials"),
        ("", "", "Invalid Credentials"),
    ],
)
def test_login_parametrized(username, password, expected):
    assert login(username, password) == expected


# ==========================================
# 7. PARALLEL TEST EXAMPLES (for pytest-xdist)
# ==========================================


@pytest.mark.parametrize("value", range(1, 6))
def test_parallel_calculation(value):
    result = value * value
    assert result == value**2


@pytest.mark.parametrize("text", ["hello", "world", "pytest", "python"])
def test_parallel_string(text):
    assert text.upper().lower() == text


# ==========================================
# COMMANDS REFERENCE
# ==========================================
#
# Run all tests:
#   pytest q3.py -v
#
# Run specific test:
#   pytest q3.py::test_addition -v
#
# Run with print output:
#   pytest q3.py -v -s
#
# Run smoke tests only:
#   pytest q3.py -m smoke -v
#
# Run regression tests:
#   pytest q3.py -m regression -v
#
# Exclude slow/regression:
#   pytest q3.py -m "not regression" -v
#
# Run in parallel (4 workers):
#   pytest q3.py -n 4 -v
#
# Generate HTML report:
#   pytest q3.py --html=report.html --self-contained-html
#
# Generate JUnit XML:
#   pytest q3.py --junitxml=results.xml
#
# Show skip/xfail reasons:
#   pytest q3.py -v -rs -rx
