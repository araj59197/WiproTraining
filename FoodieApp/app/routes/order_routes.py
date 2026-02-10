"""
Order Routes - Handles order-related API endpoints
"""

from flask import Blueprint, jsonify
from app.models import data_store

order_bp = Blueprint('order', __name__)


@order_bp.route('/api/v1/restaurants/<int:restaurant_id>/orders', methods=['GET'])
def get_orders_by_restaurant(restaurant_id):
    """View all orders for a specific restaurant"""
    if restaurant_id not in data_store.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    
    orders = [order for order in data_store.orders.values() 
              if order['restaurant_id'] == restaurant_id]
    
    return jsonify(orders), 200


@order_bp.route('/api/v1/users/<int:user_id>/orders', methods=['GET'])
def get_orders_by_user(user_id):
    """View all orders for a specific user"""
    if user_id not in data_store.users:
        return jsonify({"error": "User not found"}), 404
    
    orders = [order for order in data_store.orders.values() 
              if order['user_id'] == user_id]
    
    return jsonify(orders), 200
