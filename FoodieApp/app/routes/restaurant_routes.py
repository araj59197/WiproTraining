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


@restaurant_bp.route('/api/v1/restaurants', methods=['GET'])
def get_all_restaurants():
    """Get all restaurants with optional filtering"""
    # Get query parameters
    category = request.args.get('category')
    approved_only = request.args.get('approved', 'false').lower() == 'true'
    enabled_only = request.args.get('enabled', 'false').lower() == 'true'
    
    # Get all restaurants
    restaurants = list(data_store.restaurants.values())
    
    # Apply filters
    if category:
        restaurants = [r for r in restaurants if r['category'].lower() == category.lower()]
    
    if approved_only:
        restaurants = [r for r in restaurants if r.get('approved', False)]
    
    if enabled_only:
        restaurants = [r for r in restaurants if r.get('enabled', True)]
    
    return jsonify({
        "restaurants": restaurants,
        "count": len(restaurants)
    }), 200


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


@restaurant_bp.route('/api/v1/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    """Delete a restaurant"""
    if restaurant_id not in data_store.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    
    del data_store.restaurants[restaurant_id]
    return jsonify({"message": "Restaurant deleted successfully"}), 200


@restaurant_bp.route('/api/v1/restaurants/<int:restaurant_id>', methods=['PATCH'])
def patch_restaurant(restaurant_id):
    """Partially update restaurant details"""
    if restaurant_id not in data_store.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    
    data = request.get_json()
    restaurant = data_store.restaurants[restaurant_id]
    
    # Update only provided fields
    allowed_fields = ['name', 'category', 'location', 'contact', 'images', 'enabled', 'approved']
    for key in allowed_fields:
        if key in data:
            restaurant[key] = data[key]
            
    return jsonify(restaurant), 200


@restaurant_bp.route('/api/v1/restaurants/search', methods=['GET'])
def search_restaurants():
    """Search restaurants by name, location, or category"""
    name_query = request.args.get('name', '').lower()
    location_query = request.args.get('location', '').lower()
    category_query = request.args.get('category', '').lower()
    
    results = []
    
    for restaurant in data_store.restaurants.values():
        match = True
        
        # Check name if provided
        if name_query and name_query not in restaurant['name'].lower():
            match = False
        
        # Check location if provided
        if location_query and location_query not in restaurant['location'].lower():
            match = False
            
        # Check category if provided
        if category_query and category_query not in restaurant['category'].lower():
            match = False
            
        if match:
            results.append(restaurant)
            
    return jsonify({
        "restaurants": results,
        "count": len(results)
    }), 200
