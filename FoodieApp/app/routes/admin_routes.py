"""
Admin Routes - Handles admin-related API endpoints
"""

from flask import Blueprint, request, jsonify
from app.models import data_store

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/api/v1/admin/restaurants/<int:restaurant_id>/approve', methods=['PUT'])
def approve_restaurant(restaurant_id):
    """Approve a restaurant"""
    if restaurant_id not in data_store.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    
    data_store.restaurants[restaurant_id]['approved'] = True
    return jsonify({"message": "Restaurant approved"}), 200


@admin_bp.route('/api/v1/admin/restaurants/<int:restaurant_id>/disable', methods=['PUT'])
def admin_disable_restaurant(restaurant_id):
    """Disable a restaurant (admin endpoint)"""
    if restaurant_id not in data_store.restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    
    data_store.restaurants[restaurant_id]['enabled'] = False
    return jsonify({"message": "Restaurant disabled"}), 200


@admin_bp.route('/api/v1/admin/feedback', methods=['GET'])
def view_feedback():
    """View all customer feedback"""
    return jsonify(data_store.feedback), 200


@admin_bp.route('/api/v1/admin/orders', methods=['GET'])
def view_all_orders():
    """View all orders in the system"""
    orders_list = list(data_store.orders.values())
    return jsonify(orders_list), 200
