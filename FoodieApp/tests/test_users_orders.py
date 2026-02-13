"""
Pytest Tests for User and Order APIs
"""

import pytest
import requests

BASE_URL = "http://localhost:5000"


def test_register_user():
    """Test user registration"""
    data = {
        "name": "Aditya",
        "email": "aditya@gmail.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/users/register", json=data)
    assert response.status_code == 201
    assert response.json()['email'] == "aditya@gmail.com"
    assert 'password' not in response.json()  # Password should not be returned


def test_register_duplicate_user():
    """Test registering duplicate user returns 409"""
    data = {"name": "Jane Doe", "email": "jane@example.com", "password": "pass123"}
    requests.post(f"{BASE_URL}/api/v1/users/register", json=data)
    response = requests.post(f"{BASE_URL}/api/v1/users/register", json=data)
    assert response.status_code == 409


def test_search_restaurants():
    """Test searching restaurants"""
    # First create and approve a restaurant
    restaurant_data = {"name": "Search Test Restaurant", "category": "Indian", "location": "Mumbai", "contact": "1111111111"}
    create_response = requests.post(f"{BASE_URL}/api/v1/restaurants", json=restaurant_data)
    restaurant_id = create_response.json()['id']
    
    # Approve it (admin action)
    requests.put(f"{BASE_URL}/api/v1/admin/restaurants/{restaurant_id}/approve")
    
    # Search by location
    response = requests.get(f"{BASE_URL}/api/v1/restaurants/search?location=Mumbai")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "restaurants" in data
    assert isinstance(data["restaurants"], list)


def test_place_order():
    """Test placing an order"""
    # Create user
    user_data = {"name": "Customer", "email": "customer@example.com", "password": "pass"}
    user_response = requests.post(f"{BASE_URL}/api/v1/users/register", json=user_data)
    user_id = user_response.json()['id']
    
    # Create restaurant
    restaurant_data = {"name": "Order Restaurant", "category": "Italian", "location": "Delhi", "contact": "2222222222"}
    restaurant_response = requests.post(f"{BASE_URL}/api/v1/restaurants", json=restaurant_data)
    restaurant_id = restaurant_response.json()['id']
    
    # Place order
    order_data = {
        "user_id": user_id,
        "restaurant_id": restaurant_id,
        "dishes": [{"dish_id": 1, "quantity": 2}],
        "total": 500
    }
    response = requests.post(f"{BASE_URL}/api/v1/orders", json=order_data)
    assert response.status_code == 201
    assert response.json()['status'] == "pending"


def test_give_rating():
    """Test giving a rating"""
    # Create prerequisites (user, restaurant, order)
    user_data = {"name": "Rater", "email": "rater@example.com", "password": "pass"}
    user_response = requests.post(f"{BASE_URL}/api/v1/users/register", json=user_data)
    user_id = user_response.json()['id']
    
    restaurant_data = {"name": "Rating Restaurant", "category": "Mexican", "location": "Pune", "contact": "3333333333"}
    restaurant_response = requests.post(f"{BASE_URL}/api/v1/restaurants", json=restaurant_data)
    restaurant_id = restaurant_response.json()['id']
    
    order_data = {"user_id": user_id, "restaurant_id": restaurant_id, "dishes": [{"dish_id": 1}]}
    order_response = requests.post(f"{BASE_URL}/api/v1/orders", json=order_data)
    order_id = order_response.json()['id']
    
    # Give rating
    rating_data = {"order_id": order_id, "rating": 4.5, "comment": "Great food!"}
    response = requests.post(f"{BASE_URL}/api/v1/ratings", json=rating_data)
    assert response.status_code == 201
    assert response.json()['rating'] == 4.5


def test_invalid_rating():
    """Test invalid rating returns 400"""
    rating_data = {"order_id": 1, "rating": 6}  # Rating > 5
    response = requests.post(f"{BASE_URL}/api/v1/ratings", json=rating_data)
    assert response.status_code == 400


def test_get_orders_by_user():
    """Test getting orders by user"""
    # Create user and order
    user_data = {"name": "Order User", "email": "orderuser@example.com", "password": "pass"}
    user_response = requests.post(f"{BASE_URL}/api/v1/users/register", json=user_data)
    user_id = user_response.json()['id']
    
    restaurant_data = {"name": "Any Restaurant", "category": "Any", "location": "Any", "contact": "4444444444"}
    restaurant_response = requests.post(f"{BASE_URL}/api/v1/restaurants", json=restaurant_data)
    restaurant_id = restaurant_response.json()['id']
    
    order_data = {"user_id": user_id, "restaurant_id": restaurant_id, "dishes": []}
    requests.post(f"{BASE_URL}/api/v1/orders", json=order_data)
    
    # Get orders
    response = requests.get(f"{BASE_URL}/api/v1/users/{user_id}/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
