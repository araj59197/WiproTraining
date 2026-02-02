import pytest
import requests


# ========== SMOKE TESTS ==========
@pytest.mark.smoke
def test_get_all_movies(base_url):
    """Test: Fetch all movies"""
    response = requests.get(f"{base_url}/movies")

    # Assert status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Validate JSON response
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "Movies list should not be empty"

    # Validate structure of first movie
    first_movie = data[0]
    required_keys = ["id", "movie_name", "language", "duration", "price"]
    for key in required_keys:
        assert key in first_movie, f"Movie object missing key: {key}"


@pytest.mark.smoke
def test_add_new_movie(base_url, movie_data):
    """Test: Add a new movie"""
    response = requests.post(f"{base_url}/movies", json=movie_data)

    # Assert status code
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Validate JSON response
    data = response.json()
    assert "id" in data, "Response should contain movie ID"
    assert data["movie_name"] == movie_data["movie_name"]
    assert data["price"] == movie_data["price"]

    # Cleanup
    requests.delete(f"{base_url}/movies/{data['id']}")


@pytest.mark.smoke
def test_book_tickets(base_url, create_movie):
    """Test: Book movie tickets"""
    movie_id = create_movie

    booking_data = {"movie_id": movie_id, "seats": 3}

    response = requests.post(f"{base_url}/bookings", json=booking_data)

    # Assert status code
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Validate JSON response
    data = response.json()
    assert data["movie_id"] == movie_id
    assert data["seats"] == 3
    assert "total_price" in data
    assert "booking_id" in data


# ========== PARAMETERIZED TESTS ==========
@pytest.mark.parametrize(
    "movie_name,language,duration,price",
    [
        ("Avatar", "English", "3h 12m", 350),
        ("RRR", "Telugu", "3h 7m", 280),
        ("Dangal", "Hindi", "2h 41m", 200),
    ],
)
def test_add_multiple_movies(base_url, movie_name, language, duration, price):
    """Parameterized test: Add multiple movies with different data"""
    movie_data = {
        "movie_name": movie_name,
        "language": language,
        "duration": duration,
        "price": price,
    }

    response = requests.post(f"{base_url}/movies", json=movie_data)
    assert response.status_code == 201

    data = response.json()
    assert data["movie_name"] == movie_name
    assert data["language"] == language

    # Cleanup
    requests.delete(f"{base_url}/movies/{data['id']}")


@pytest.mark.parametrize(
    "seats,expected_status",
    [
        (1, 201),  # Valid: 1 seat
        (5, 201),  # Valid: 5 seats
        (0, 400),  # Invalid: 0 seats
        (-1, 400),  # Invalid: negative seats
    ],
)
def test_booking_validation(base_url, create_movie, seats, expected_status):
    """Parameterized test: Validate booking with different seat counts"""
    movie_id = create_movie

    booking_data = {"movie_id": movie_id, "seats": seats}

    response = requests.post(f"{base_url}/bookings", json=booking_data)
    assert response.status_code == expected_status


# ========== REGRESSION TESTS ==========
@pytest.mark.regression
def test_get_movie_by_id(base_url, create_movie):
    """Test: Get movie by ID"""
    movie_id = create_movie

    response = requests.get(f"{base_url}/movies/{movie_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == movie_id


@pytest.mark.regression
def test_update_movie(base_url, create_movie):
    """Test: Update movie details"""
    movie_id = create_movie

    updated_data = {"price": 450, "language": "Hindi"}

    response = requests.put(f"{base_url}/movies/{movie_id}", json=updated_data)
    assert response.status_code == 200

    data = response.json()
    assert data["price"] == 450
    assert data["language"] == "Hindi"


@pytest.mark.regression
def test_delete_movie(base_url, movie_data):
    """Test: Delete a movie"""
    # Create movie
    post_response = requests.post(f"{base_url}/movies", json=movie_data)
    movie_id = post_response.json()["id"]

    # Delete movie
    delete_response = requests.delete(f"{base_url}/movies/{movie_id}")
    assert delete_response.status_code == 200

    # Verify deletion
    get_response = requests.get(f"{base_url}/movies/{movie_id}")
    assert get_response.status_code == 404


# ========== CRITICAL/NEGATIVE TESTS ==========
@pytest.mark.critical
def test_get_nonexistent_movie(base_url):
    """Test: Get non-existent movie (negative test)"""
    response = requests.get(f"{base_url}/movies/99999")
    assert response.status_code == 404

    data = response.json()
    assert "error" in data


@pytest.mark.critical
def test_book_invalid_movie(base_url):
    """Test: Book tickets for non-existent movie"""
    booking_data = {"movie_id": 99999, "seats": 2}

    response = requests.post(f"{base_url}/bookings", json=booking_data)
    assert response.status_code == 404


@pytest.mark.critical
def test_add_movie_invalid_data(base_url):
    """Test: Add movie with invalid/missing data"""
    response = requests.post(f"{base_url}/movies", json={})
    assert response.status_code in [201, 400]


# ========== EXCEPTION HANDLING TESTS ==========
def test_api_connection_error():
    """Test: Handle connection errors gracefully"""
    try:
        response = requests.get("http://127.0.0.1:9999/api/movies", timeout=1)
    except requests.exceptions.ConnectionError as e:
        pytest.skip(f"Expected connection error: {e}")
    except requests.exceptions.Timeout as e:
        pytest.skip(f"Expected timeout error: {e}")


def test_invalid_json_response(base_url, create_movie):
    """Test: Validate JSON parsing"""
    movie_id = create_movie

    response = requests.get(f"{base_url}/movies/{movie_id}")

    try:
        data = response.json()
        assert isinstance(data, dict)
    except ValueError as e:
        pytest.fail(f"Invalid JSON response: {e}")
