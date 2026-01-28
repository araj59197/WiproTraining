import pytest
import sys


@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
    (-5, -5, -10),
])
def test_addition(a, b, expected):
    assert a + b == expected


@pytest.mark.parametrize("x, y, result", [
    (2, 3, 6),
    (0, 100, 0),
    (-2, 3, -6),
    (7, 7, 49),
])
def test_multiplication(x, y, result):
    assert x * y == result


@pytest.mark.parametrize("input_str, expected_upper", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("PyTest", "PYTEST"),
    ("", ""),
])
def test_string_upper(input_str, expected_upper):
    assert input_str.upper() == expected_upper


def test_with_custom_option(custom_option):
    print(f"\nCustom option value: {custom_option}")
    assert custom_option is not None


def test_environment_mode(env_mode):
    print(f"\nRunning in environment: {env_mode}")
    assert env_mode in ["dev", "staging", "prod"]


def test_config_value(pytestconfig):
    markers = pytestconfig.getini("markers")
    print(f"\nRegistered markers: {markers}")
    assert markers is not None


def test_minimum_version(pytestconfig):
    min_version = pytestconfig.getini("minversion")
    print(f"\nMinimum pytest version required: {min_version}")


@pytest.mark.skip(reason="This test is skipped intentionally for demonstration")
def test_skipped():
    assert True


@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_python_310_feature():
    value = 1
    match value:
        case 1:
            result = "one"
        case _:
            result = "other"
    assert result == "one"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-only test")
def test_windows_only():
    import os
    assert os.name == "nt"


@pytest.mark.xfail(reason="This test demonstrates expected failure")
def test_expected_failure():
    assert 1 == 2


@pytest.mark.xfail(strict=True, reason="Must fail, otherwise test fails")
def test_strict_xfail():
    assert 1 == 2


@pytest.mark.xfail(sys.version_info < (3, 12), reason="Known issue in Python < 3.12")
def test_conditional_xfail():
    assert True


@pytest.mark.xfail(reason="Expected to fail but might pass")
def test_xfail_but_passes():
    assert 1 == 1


@pytest.mark.parametrize("divisor", [1, 2, 0, 5])
def test_division_with_skip(divisor):
    if divisor == 0:
        pytest.skip("Cannot divide by zero")
    result = 10 / divisor
    assert result == 10 / divisor


@pytest.mark.parametrize("value, expected", [
    (1, 1),
    pytest.param(2, 3, marks=pytest.mark.xfail(reason="Intentionally wrong")),
    (3, 3),
    pytest.param(4, 5, marks=pytest.mark.skip(reason="Skipped test case")),
])
def test_parameterized_with_markers(value, expected):
    assert value == expected


@pytest.mark.slow
def test_slow_operation():
    import time
    time.sleep(0.1)
    assert True


@pytest.mark.smoke
def test_smoke_test():
    assert 1 + 1 == 2


@pytest.mark.regression
def test_regression():
    assert "hello".replace("e", "a") == "hallo"