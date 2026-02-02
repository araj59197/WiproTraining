import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:5001/api"

@pytest.fixture(scope="session")
def base_url():
    """Fixture to provide base URL for all tests"""
    return BASE_URL

@pytest.fixture(scope="function")
def movie_data():
    """Fixture to provide sample movie data"""
    return {
        "movie_name": "The Dark Knight",
        "language": "English",
        "duration": "2h 32m",
        "price": 300
    }

@pytest.fixture(scope="function")
def create_movie(base_url, movie_data):
    """Fixture to create a movie and return its ID (setup/teardown)"""
    # Setup: Create movie
    response = requests.post(f"{base_url}/movies", json=movie_data)
    movie_id = response.json().get("id")
    
    yield movie_id  # Provide movie_id to test
    
    # Teardown: Delete movie after test
    try:
        requests.delete(f"{base_url}/movies/{movie_id}")
    except:
        pass  # Ignore errors if movie already deleted

@pytest.fixture(scope="session", autouse=True)
def check_api_status(base_url):
    """Session-level fixture to verify API is running"""
    max_retries = 3
    for i in range(max_retries):
        try:
            response = requests.get(f"{base_url}/movies", timeout=2)
            if response.status_code == 200:
                print(f"\n✓ API is running at {base_url}")
                return
        except requests.exceptions.RequestException:
            if i < max_retries - 1:
                print(f"\n⚠ Waiting for API to start... (attempt {i+1}/{max_retries})")
                time.sleep(2)
    
    pytest.fail(f"API is not running at {base_url}. Please start the Flask server.")
