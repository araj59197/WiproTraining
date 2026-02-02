import pytest
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://127.0.0.1:5002"


@pytest.mark.web
def test_scrape_patient_names():
    """Test: Extract patient names from HTML"""
    response = requests.get(f"{BASE_URL}/patients")
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")

    # Find all patient name cells
    name_cells = soup.find_all("td", class_="patient-name")
    assert len(name_cells) > 0, "No patient names found"

    names = [cell.text.strip() for cell in name_cells]
    print(f"\n📋 Patient Names: {names}")
    assert all(name for name in names), "Some names are empty"


@pytest.mark.web
def test_scrape_patient_ages():
    """Test: Extract patient ages from HTML"""
    response = requests.get(f"{BASE_URL}/patients")
    soup = BeautifulSoup(response.content, "html.parser")

    age_cells = soup.find_all("td", class_="patient-age")
    ages = [cell.text.strip() for cell in age_cells]

    print(f"\n📊 Patient Ages: {ages}")
    # Check if ages can be converted to integers (including negative)
    for age in ages:
        try:
            int(age)
        except ValueError:
            pytest.fail(f"Invalid age format: {age}")


@pytest.mark.web
def test_scrape_patient_diseases():
    """Test: Extract diseases from HTML"""
    response = requests.get(f"{BASE_URL}/patients")
    soup = BeautifulSoup(response.content, "html.parser")

    disease_cells = soup.find_all("td", class_="patient-disease")
    diseases = [cell.text.strip() for cell in disease_cells]

    print(f"\n🏥 Diseases: {diseases}")
    assert len(diseases) > 0, "No diseases found"


@pytest.mark.web
def test_scrape_assigned_doctors():
    """Test: Extract assigned doctors from HTML"""
    response = requests.get(f"{BASE_URL}/patients")
    soup = BeautifulSoup(response.content, "html.parser")

    doctor_cells = soup.find_all("td", class_="patient-doctor")
    doctors = [cell.text.strip() for cell in doctor_cells]

    print(f"\n👨‍⚕️ Assigned Doctors: {doctors}")
    assert all(doctor.startswith("Dr.") for doctor in doctors), "Invalid doctor format"


@pytest.mark.web
def test_scrape_complete_patient_data():
    """Test: Extract all patient data and validate structure"""
    response = requests.get(f"{BASE_URL}/patients")
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all patient rows
    patient_rows = soup.find_all("tr", class_="patient-row")

    patients_data = []
    for row in patient_rows:
        cells = row.find_all("td")
        patient = {
            "name": cells[1].text.strip(),
            "age": cells[2].text.strip(),
            "disease": cells[5].text.strip(),
            "doctor": cells[6].text.strip(),
        }
        patients_data.append(patient)

    print(f"\n📋 Complete Patient Data:")
    for patient in patients_data:
        print(
            f"  • {patient['name']}, Age: {patient['age']}, Disease: {patient['disease']}, Doctor: {patient['doctor']}"
        )

    assert len(patients_data) > 0, "No patient data extracted"


@pytest.mark.web
@pytest.mark.slow
def test_web_page_has_form():
    """Test: Verify registration form exists"""
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    # Check form exists
    form = soup.find("form", {"id": "patientForm"})
    assert form is not None, "Registration form not found"

    # Check form fields
    name_field = soup.find("input", {"id": "name"})
    age_field = soup.find("input", {"id": "age"})
    disease_field = soup.find("input", {"id": "disease"})
    doctor_dropdown = soup.find("select", {"id": "doctor"})

    assert name_field is not None, "Name field not found"
    assert age_field is not None, "Age field not found"
    assert disease_field is not None, "Disease field not found"
    assert doctor_dropdown is not None, "Doctor dropdown not found"

    print("\n✓ All form fields found")
