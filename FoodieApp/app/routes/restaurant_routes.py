"""
Restaurant Routes - Handles restaurant-related API endpoints
"""

from flask import Blueprint, request, jsonify
from app.models import data_store
from app.services.validation import validate_restaurant_data

restaurant_bp = Blueprint('restaurant', __name__)


@restaurant_bp.route('/api/v1/restaurants', methods=['POST'])
def register_restaurant():
    """Register a new restaurant"""
    data = request.get_json()
    
    # Validate input
    is_valid, error_msg = validate_restaurant_data(data)
    if not is_valid:
        return jsonify({"error": error_msg}), 400
    
    # Check for duplicate name
    for restaurant in data_store.restaurants.values():
        if restaurant['name'] == data['name']:
            return jsonify({"error": "Restaurant with this name already exists"}), 409
    
    # Create restaurant
    restaurant_id = data_store.get_next_restaurant_id()
    restaurant = {
        "id": restaurant_id,
        "name": data['name'],
        "category": data['category'],
        "location": data['location'],
        "contact": data['contact'],
        "images": data.get('images', []),
        "enabled": True,
        "approved": False
    }
    
    data_store.restaurants[restaurant_id] = restaurant
    return jsonify(restaurant), 201


@restaurant_bp.route('/api/v1/restaurants/<int:restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    """Update restaurant details"""
    if restaurant_id not in data_store.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    
    data = request.get_json()
    restaurant = data_store.restaurants[restaurant_id]
    
    # Update fields
    for key in ['name', 'category', 'location', 'contact', 'images']:
        if key in data:
            restaurant[key] = data[key]
    
    return jsonify(restaurant), 200


@restaurant_bp.route('/api/v1/restaurants/<int:restaurant_id>/disable', methods=['PUT'])
def disable_restaurant(restaurant_id):
    """Disable a restaurant"""
    if restaurant_id not in data_store.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    
    data_store.restaurants[restaurant_id]['enabled'] = False
    return jsonify({"message": "Restaurant disabled"}), 200


@restaurant_bp.route('/api/v1/restaurants/<int:restaurant_id>', methods=['GET'])
def view_restaurant(restaurant_id):
    """View restaurant profile"""
    if restaurant_id not in data_store.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    
    return jsonify(data_store.restaurants[restaurant_id]), 200
