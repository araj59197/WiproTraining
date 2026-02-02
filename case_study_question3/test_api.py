import pytest
import requests


# ========== SMOKE TESTS ==========
@pytest.mark.smoke
@pytest.mark.api
def test_get_all_patients(base_url):
    """Test: Fetch all patients"""
    response = requests.get(f"{base_url}/patients")

    # Validate status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Validate JSON response
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "Patients list should not be empty"

    # Validate structure
    first_patient = data[0]
    required_keys = ["id", "name", "age", "gender", "contact", "disease", "doctor"]
    for key in required_keys:
        assert key in first_patient, f"Patient object missing key: {key}"


@pytest.mark.smoke
@pytest.mark.api
def test_register_patient(base_url, patient_data):
    """Test: Register a new patient"""
    response = requests.post(f"{base_url}/patients", json=patient_data)

    # Validate status code
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Validate JSON response
    data = response.json()
    assert "id" in data, "Response should contain patient ID"
    assert data["name"] == patient_data["name"]
    assert data["age"] == patient_data["age"]
    assert data["disease"] == patient_data["disease"]


@pytest.mark.smoke
@pytest.mark.api
def test_get_patient_by_id(base_url, create_patient):
    """Test: Get patient details by ID"""
    patient_id = create_patient

    response = requests.get(f"{base_url}/patients/{patient_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == patient_id


# ========== PARAMETERIZED TESTS ==========
@pytest.mark.parametrize(
    "name,age,gender,disease,doctor",
    [
        ("Alice Johnson", 28, "Female", "Asthma", "Dr. Smith"),
        ("Bob Williams", 55, "Male", "Heart Disease", "Dr. Johnson"),
        ("Charlie Brown", 40, "Male", "Arthritis", "Dr. Williams"),
    ],
)
@pytest.mark.api
def test_register_multiple_patients(base_url, name, age, gender, disease, doctor):
    """Parameterized test: Register multiple patients"""
    patient_data = {
        "name": name,
        "age": age,
        "gender": gender,
        "contact": "9999999999",
        "disease": disease,
        "doctor": doctor,
    }

    response = requests.post(f"{base_url}/patients", json=patient_data)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == name
    assert data["age"] == age
    assert data["disease"] == disease


# ========== REGRESSION TESTS ==========
@pytest.mark.regression
@pytest.mark.api
def test_update_patient_info(base_url, create_patient):
    """Test: Update patient information"""
    patient_id = create_patient

    updated_data = {"disease": "Recovered", "doctor": "Dr. Brown"}

    response = requests.put(f"{base_url}/patients/{patient_id}", json=updated_data)
    assert response.status_code == 200

    data = response.json()
    assert data["disease"] == "Recovered"
    assert data["doctor"] == "Dr. Brown"


# ========== NEGATIVE TESTS ==========
@pytest.mark.critical
@pytest.mark.api
def test_get_nonexistent_patient(base_url):
    """Negative test: Get non-existent patient"""
    response = requests.get(f"{base_url}/patients/99999")
    assert response.status_code == 404

    data = response.json()
    assert "error" in data


@pytest.mark.critical
@pytest.mark.api
def test_register_patient_missing_name(base_url):
    """Negative test: Register patient without name"""
    invalid_data = {"age": 30, "gender": "Male"}

    response = requests.post(f"{base_url}/patients", json=invalid_data)
    assert response.status_code == 400


@pytest.mark.critical
@pytest.mark.api
def test_update_nonexistent_patient(base_url):
    """Negative test: Update non-existent patient"""
    response = requests.put(f"{base_url}/patients/99999", json={"disease": "Flu"})
    assert response.status_code == 404


# ========== HEADERS AND REQUEST VALIDATION ==========
@pytest.mark.api
def test_api_with_custom_headers(base_url, patient_data):
    """Test: Send request with custom headers"""
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Hospital-Test-Suite/1.0",
    }

    response = requests.post(f"{base_url}/patients", json=patient_data, headers=headers)
    assert response.status_code == 201


# ========== JSON DESERIALIZATION TESTS ==========
@pytest.mark.api
def test_json_deserialization(base_url):
    """Test: Validate JSON deserialization"""
    response = requests.get(f"{base_url}/patients")

    # Test JSON parsing
    try:
        data = response.json()
        assert isinstance(data, list)

        # Verify JSON structure
        for patient in data:
            assert isinstance(patient["id"], int)
            assert isinstance(patient["name"], str)
            assert isinstance(patient["age"], int)
    except ValueError as e:
        pytest.fail(f"Invalid JSON response: {e}")


# ========== SKIP AND XFAIL TESTS ==========
@pytest.mark.skip(reason="DELETE endpoint not implemented yet")
@pytest.mark.api
def test_delete_patient(base_url, create_patient):
    """Test: Delete patient (skipped - not implemented)"""
    patient_id = create_patient
    response = requests.delete(f"{base_url}/patients/{patient_id}")
    assert response.status_code == 200


@pytest.mark.xfail(reason="Known issue: API doesn't validate age range")
@pytest.mark.api
def test_register_patient_invalid_age(base_url):
    """Test: Register patient with invalid age (expected to fail)"""
    invalid_data = {
        "name": "Invalid Patient",
        "age": -5,  # Negative age
        "gender": "Male",
        "contact": "1234567890",
        "disease": "Test",
        "doctor": "Dr. Smith",
    }

    response = requests.post(f"{base_url}/patients", json=invalid_data)
    assert response.status_code == 400  # Expected to fail


# ========== EXCEPTION HANDLING ==========
@pytest.mark.api
def test_connection_error_handling():
    """Test: Handle connection errors"""
    try:
        response = requests.get("http://127.0.0.1:9999/api/patients", timeout=1)
    except requests.exceptions.ConnectionError:
        pytest.skip("Expected connection error - test passed")
    except requests.exceptions.Timeout:
        pytest.skip("Expected timeout - test passed")
