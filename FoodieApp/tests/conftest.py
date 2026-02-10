"""
Pytest configuration and fixtures for Foodie App tests
"""

import pytest
import requests

BASE_URL = "http://localhost:5000"


@pytest.fixture(autouse=True)
def reset_data_before_test():
    """Reset data store before each test to ensure clean state"""
    try:
        response = requests.post(f"{BASE_URL}/reset")
        if response.status_code != 200:
            print(f"Warning: Failed to reset data - {response.status_code}")
    except requests.exceptions.ConnectionError:
        pytest.skip("Flask server is not running. Start with: python run.py")
    yield
