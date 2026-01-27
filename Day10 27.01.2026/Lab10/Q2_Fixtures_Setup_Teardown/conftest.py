import pytest


@pytest.fixture(scope="module")
def module_data():
    print("\n[MODULE FIXTURE] Setting up module data...")
    data = {"app_name": "Calculator", "version": "1.0"}
    yield data
    print("\n[MODULE FIXTURE] Tearing down module data...")


@pytest.fixture(scope="function")
def sample_numbers():
    print("\n[FUNCTION FIXTURE] Preparing sample numbers...")
    numbers = {"a": 10, "b": 5}
    yield numbers
    print("\n[FUNCTION FIXTURE] Cleaning up sample numbers...")


@pytest.fixture
def division_data():
    print("\n[FUNCTION FIXTURE] Preparing division test data...")
    yield {"dividend": 20, "divisor": 4, "expected": 5.0}
    print("\n[FUNCTION FIXTURE] Cleaning up division data...")
