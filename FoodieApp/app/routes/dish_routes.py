"""
Dish Routes - Handles dish-related API endpoints
"""

from flask import Blueprint, request, jsonify
from app.models import data_store
from app.services.validation import validate_dish_data

dish_bp = Blueprint('dish', __name__)


@dish_bp.route('/api/v1/restaurants/<int:restaurant_id>/dishes', methods=['POST'])
def add_dish(restaurant_id):
    """Add a new dish to a restaurant"""
    if restaurant_id not in data_store.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    
    data = request.get_json()
    
    # Validate input
    is_valid, error_msg = validate_dish_data(data)
    if not is_valid:
        return jsonify({"error": error_msg}), 400
    
    # Create dish
    dish_id = data_store.get_next_dish_id()
    dish = {
        "id": dish_id,
        "restaurant_id": restaurant_id,
        "name": data['name'],
        "type": data['type'],
        "price": data['price'],
        "available_time": data.get('available_time', 'All day'),
        "image": data.get('image', ''),
        "enabled": True
    }
    
    data_store.dishes[dish_id] = dish
    return jsonify(dish), 201


@dish_bp.route('/api/v1/dishes/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    """Update dish details"""
    if dish_id not in data_store.dishes:
        return jsonify({"error": "Dish not found"}), 404
    
    data = request.get_json()
    dish = data_store.dishes[dish_id]
    
    # Update fields
    for key in ['name', 'type', 'price', 'available_time', 'image']:
        if key in data:
            dish[key] = data[key]
    
    return jsonify(dish), 200


@dish_bp.route('/api/v1/dishes/<int:dish_id>/status', methods=['PUT'])
def toggle_dish_status(dish_id):
    """Enable or disable a dish"""
    if dish_id not in data_store.dishes:
        return jsonify({"error": "Dish not found"}), 404
    
    data = request.get_json()
    if 'enabled' not in data:
        return jsonify({"error": "enabled field is required"}), 400
    
    data_store.dishes[dish_id]['enabled'] = data['enabled']
    status = "enabled" if data['enabled'] else "disabled"
    return jsonify({"message": f"Dish {status}"}), 200


@dish_bp.route('/api/v1/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    """Delete a dish"""
    if dish_id not in data_store.dishes:
        return jsonify({"error": "Dish not found"}), 404
    
    del data_store.dishes[dish_id]
    return jsonify({"message": "Dish deleted"}), 200
