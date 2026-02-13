"""
User Routes - Handles user-related API endpoints
"""

from flask import Blueprint, request, jsonify
from app.models import data_store
from app.services.validation import validate_user_data, validate_order_data, validate_rating_data

user_bp = Blueprint('user', __name__)


@user_bp.route('/api/v1/users/register', methods=['POST'])
def register_user():
    """Register a new user"""
    data = request.get_json()
    
    # Validate input
    is_valid, error_msg = validate_user_data(data)
    if not is_valid:
        return jsonify({"error": error_msg}), 400
    
    # Check for duplicate email
    for user in data_store.users.values():
        if user['email'] == data['email']:
            return jsonify({"error": "User with this email already exists"}), 409
    
    # Create user
    user_id = data_store.get_next_user_id()
    user = {
        "id": user_id,
        "name": data['name'],
        "email": data['email'],
        "password": data['password']  # In production, hash this!
    }
    
    data_store.users[user_id] = user
    # Don't return password
    user_response = {k: v for k, v in user.items() if k != 'password'}
    return jsonify(user_response), 201


@user_bp.route('/api/v1/restaurants/search', methods=['GET'])
def search_restaurants():
    """Search restaurants by name, location, dish, or rating"""
    name = request.args.get('name', '').lower()
    location = request.args.get('location', '').lower()
    dish = request.args.get('dish', '').lower()
    min_rating = request.args.get('rating', type=float)
    include_unapproved = request.args.get('include_unapproved', 'false').lower() == 'true'
    
    results = []
    
    for restaurant in data_store.restaurants.values():
        # Skip disabled restaurants (always)
        if not restaurant['enabled']:
            continue
        
        # Skip unapproved restaurants unless include_unapproved=true
        if not include_unapproved and not restaurant['approved']:
            continue
        
        # Filter by name
        if name and name not in restaurant['name'].lower():
            continue
        
        # Filter by location
        if location and location not in restaurant['location'].lower():
            continue
        
        # Get all dishes for this restaurant
        restaurant_dishes = [d for d in data_store.dishes.values() 
                            if d['restaurant_id'] == restaurant['id']]
        
        # Filter by dish
        if dish:
            has_dish = any(dish in d['name'].lower() for d in restaurant_dishes)
            if not has_dish:
                continue
        
        # Calculate average rating and get all ratings
        restaurant_ratings = [r for r in data_store.ratings.values() 
                            if data_store.orders.get(r['order_id'], {}).get('restaurant_id') == restaurant['id']]
        
        if restaurant_ratings:
            avg_rating = sum(r['rating'] for r in restaurant_ratings) / len(restaurant_ratings)
        else:
            avg_rating = 0
        
        # Filter by rating
        if min_rating and avg_rating < min_rating:
            continue
        
        # Build detailed result
        result = {
            "id": restaurant['id'],
            "name": restaurant['name'],
            "category": restaurant['category'],
            "location": restaurant['location'],
            "contact": restaurant['contact'],
            "images": restaurant.get('images', []),
            "average_rating": round(avg_rating, 2),
            "total_ratings": len(restaurant_ratings),
            "dishes": [
                {
                    "id": d['id'],
                    "name": d['name'],
                    "type": d['type'],
                    "price": d['price'],
                    "available_time": d.get('available_time', 'All day'),
                    "image": d.get('image', ''),
                    "enabled": d.get('enabled', True)
                }
                for d in restaurant_dishes
            ],
            "total_dishes": len(restaurant_dishes),
            "recent_ratings": [
                {
                    "rating": r['rating'],
                    "comment": r.get('comment', '')
                }
                for r in restaurant_ratings[:5]  # Show last 5 ratings
            ]
        }
        results.append(result)
    
    return jsonify({
        "restaurants": results,
        "count": len(results)
    }), 200


@user_bp.route('/api/v1/orders', methods=['POST'])
def place_order():
    """Place a new order"""
    data = request.get_json()
    
    # Validate input
    is_valid, error_msg = validate_order_data(data)
    if not is_valid:
        return jsonify({"error": error_msg}), 400
    
    # Validate user exists
    if data['user_id'] not in data_store.users:
        return jsonify({"error": "User not found"}), 400
    
    # Validate restaurant exists
    if data['restaurant_id'] not in data_store.restaurants:
        return jsonify({"error": "Restaurant not found"}), 400
    
    # Create order
    order_id = data_store.get_next_order_id()
    order = {
        "id": order_id,
        "user_id": data['user_id'],
        "restaurant_id": data['restaurant_id'],
        "dishes": data['dishes'],
        "status": "pending",
        "total": data.get('total', 0)
    }
    
    data_store.orders[order_id] = order
    return jsonify(order), 201


@user_bp.route('/api/v1/ratings', methods=['POST'])
def give_rating():
    """Give a rating to an order"""
    data = request.get_json()
    
    # Validate input
    is_valid, error_msg = validate_rating_data(data)
    if not is_valid:
        return jsonify({"error": error_msg}), 400
    
    # Validate order exists
    if data['order_id'] not in data_store.orders:
        return jsonify({"error": "Order not found"}), 400
    
    # Create rating
    rating_id = data_store.get_next_rating_id()
    rating = {
        "id": rating_id,
        "order_id": data['order_id'],
        "rating": data['rating'],
        "comment": data.get('comment', '')
    }
    
    data_store.ratings[rating_id] = rating
    
    # Add to feedback
    order = data_store.orders[data['order_id']]
    feedback_entry = {
        "rating_id": rating_id,
        "user_id": order['user_id'],
        "restaurant_id": order['restaurant_id'],
        "rating": rating['rating'],
        "comment": rating['comment']
    }
    data_store.feedback.append(feedback_entry)
    
    return jsonify(rating), 201
