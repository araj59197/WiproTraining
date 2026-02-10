"""
Validation utilities for input validation
"""


def validate_restaurant_data(data):
    """Validate restaurant registration data"""
    required_fields = ['name', 'category', 'location', 'contact']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    return True, None


def validate_dish_data(data):
    """Validate dish data"""
    required_fields = ['name', 'type', 'price']
    for field in required_fields:
        if field not in data or data[field] is None:
            return False, f"Missing required field: {field}"
    return True, None


def validate_user_data(data):
    """Validate user registration data"""
    required_fields = ['name', 'email', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    return True, None


def validate_order_data(data):
    """Validate order data"""
    required_fields = ['user_id', 'restaurant_id', 'dishes']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    if not isinstance(data['dishes'], list) or len(data['dishes']) == 0:
        return False, "Dishes must be a non-empty list"
    return True, None


def validate_rating_data(data):
    """Validate rating data"""
    required_fields = ['order_id', 'rating']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    if not isinstance(data['rating'], (int, float)) or data['rating'] < 1 or data['rating'] > 5:
        return False, "Rating must be between 1 and 5"
    return True, None
