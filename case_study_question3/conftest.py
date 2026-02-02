import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:5002/api"


@pytest.fixture(scope="session")
def base_url():
    """Fixture to provide base URL for all tests"""
    return BASE_URL


@pytest.fixture(scope="function")
def patient_data():
    """Fixture to provide sample patient data"""
    return {
        "name": "Test Patient",
        "age": 30,
        "gender": "Male",
        "contact": "1234567890",
        "disease": "Flu",
        "doctor": "Dr. Smith",
    }


@pytest.fixture(scope="function")
def create_patient(base_url, patient_data):
    """Fixture to create a patient and return ID (setup/teardown)"""
    # Setup: Create patient
    response = requests.post(f"{base_url}/patients", json=patient_data)
    patient_id = response.json().get("id")

    yield patient_id  # Provide patient_id to test

    # Note: No teardown deletion as API doesn't have DELETE endpoint


@pytest.fixture(scope="session", autouse=True)
def check_api_status(base_url):
    """Session-level fixture to verify API is running"""
    max_retries = 3
    for i in range(max_retries):
        try:
            response = requests.get(f"{base_url}/patients", timeout=2)
            if response.status_code == 200:
                print(f"\n✓ Hospital API is running at {base_url}")
                return
        except requests.exceptions.RequestException:
            if i < max_retries - 1:
                print(f"\n⚠ Waiting for API to start... (attempt {i+1}/{max_retries})")
                time.sleep(2)

    pytest.fail(f"API is not running at {base_url}. Please start: python app.py")
