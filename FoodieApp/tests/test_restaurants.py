"""
Pytest Tests for Restaurant APIs
"""

import pytest
import requests

BASE_URL = "http://localhost:5000"


def test_register_restaurant():
    """Test registering a new restaurant"""
    data = {
        "name": "Food Hub",
        "category": "Indian",
        "location": "Mumbai",
        "contact": "1234567890"
    }
    response = requests.post(f"{BASE_URL}/api/v1/restaurants", json=data)
    assert response.status_code == 201
    assert response.json()['name'] == "Food Hub"


def test_register_duplicate_restaurant():
    """Test registering duplicate restaurant returns 409"""
    data = {
        "name": "Food Hub",
        "category": "Indian",
        "location": "Mumbai",
        "contact": "1234567890"
    }
    # First registration
    requests.post(f"{BASE_URL}/api/v1/restaurants", json=data)
    # Duplicate registration
    response = requests.post(f"{BASE_URL}/api/v1/restaurants", json=data)
    assert response.status_code == 409


def test_register_restaurant_missing_field():
    """Test registering restaurant with missing field returns 400"""
    data = {
        "name": "Incomplete Restaurant",
        "category": "Italian"
        # Missing location and contact
    }
    response = requests.post(f"{BASE_URL}/api/v1/restaurants", json=data)
    assert response.status_code == 400


def test_update_restaurant():
    """Test updating restaurant details"""
    # First create a restaurant
    data = {"name": "Test Restaurant", "category": "Chinese", "location": "Delhi", "contact": "9876543210"}
    create_response = requests.post(f"{BASE_URL}/api/v1/restaurants", json=data)
    restaurant_id = create_response.json()['id']
    
    # Update it
    update_data = {"category": "Pan-Asian"}
    response = requests.put(f"{BASE_URL}/api/v1/restaurants/{restaurant_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()['category'] == "Pan-Asian"


def test_update_nonexistent_restaurant():
    """Test updating nonexistent restaurant returns 404"""
    response = requests.put(f"{BASE_URL}/api/v1/restaurants/9999", json={"name": "New Name"})
    assert response.status_code == 404


def test_disable_restaurant():
    """Test disabling a restaurant"""
    # First create a restaurant
    data = {"name": "To Disable", "category": "Fast Food", "location": "Pune", "contact": "5555555555"}
    create_response = requests.post(f"{BASE_URL}/api/v1/restaurants", json=data)
    restaurant_id = create_response.json()['id']
    
    # Disable it
    response = requests.put(f"{BASE_URL}/api/v1/restaurants/{restaurant_id}/disable")
    assert response.status_code == 200
    assert response.json()['message'] == "Restaurant disabled"


def test_view_restaurant():
    """Test viewing restaurant profile"""
    # First create a restaurant
    data = {"name": "View Test", "category": "Cafe", "location": "Bangalore", "contact": "4444444444"}
    create_response = requests.post(f"{BASE_URL}/api/v1/restaurants", json=data)
    restaurant_id = create_response.json()['id']
    
    # View it
    response = requests.get(f"{BASE_URL}/api/v1/restaurants/{restaurant_id}")
    assert response.status_code == 200
    assert response.json()['name'] == "View Test"


def test_view_nonexistent_restaurant():
    """Test viewing nonexistent restaurant returns 404"""
    response = requests.get(f"{BASE_URL}/api/v1/restaurants/9999")
    assert response.status_code == 404
