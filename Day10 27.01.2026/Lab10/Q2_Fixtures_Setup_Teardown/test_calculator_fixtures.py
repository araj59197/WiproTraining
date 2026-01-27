import pytest
from calculator import add, subtract, multiply, divide

def setup_module(module):
    print("\n===== SETUP MODULE: Starting test module =====")


def teardown_module(module):
    print("\n===== TEARDOWN MODULE: Finished test module =====")


def setup_function(function):
    print(f"\n--- setup_function: Preparing for {function.__name__} ---")


def teardown_function(function):
    print(f"--- teardown_function: Cleaning after {function.__name__} ---")
def test_add_with_fixture(sample_numbers):
    print(f"Testing add with {sample_numbers}")
    result = add(sample_numbers["a"], sample_numbers["b"])
    assert result == 15
    print(f"{sample_numbers['a']} + {sample_numbers['b']} = {result} ✓")


def test_subtract_with_fixture(sample_numbers):
    print(f"Testing subtract with {sample_numbers}")
    result = subtract(sample_numbers["a"], sample_numbers["b"])
    assert result == 5
    print(f"{sample_numbers['a']} - {sample_numbers['b']} = {result} ✓")


def test_multiply_with_fixture(sample_numbers):
    print(f"Testing multiply with {sample_numbers}")
    result = multiply(sample_numbers["a"], sample_numbers["b"])
    assert result == 50
    print(f"{sample_numbers['a']} * {sample_numbers['b']} = {result} ✓")


def test_divide_with_fixture(division_data):
    print(f"Testing divide with {division_data}")
    result = divide(division_data["dividend"], division_data["divisor"])
    assert result == division_data["expected"]
    print(f"{division_data['dividend']} / {division_data['divisor']} = {result} ✓")


def test_module_scope_fixture(module_data):
    print(f"Using module data: {module_data}")
    assert module_data["app_name"] == "Calculator"
    assert module_data["version"] == "1.0"
    print("Module fixture data verified ✓")


def test_module_scope_fixture_again(module_data):
    print(f"Reusing module data: {module_data}")
    assert "app_name" in module_data
    print("Module fixture reused (same instance) ✓")
