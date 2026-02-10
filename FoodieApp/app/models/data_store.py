"""
Data Store Module - In-memory data storage for Foodie App
"""

# In-memory data stores
restaurants = {}
dishes = {}
users = {}
orders = {}
ratings = {}
feedback = []

# ID counters
restaurant_id_counter = 1
dish_id_counter = 1
user_id_counter = 1
order_id_counter = 1
rating_id_counter = 1


def get_next_restaurant_id():
    global restaurant_id_counter
    current = restaurant_id_counter
    restaurant_id_counter += 1
    return current


def get_next_dish_id():
    global dish_id_counter
    current = dish_id_counter
    dish_id_counter += 1
    return current


def get_next_user_id():
    global user_id_counter
    current = user_id_counter
    user_id_counter += 1
    return current


def get_next_order_id():
    global order_id_counter
    current = order_id_counter
    order_id_counter += 1
    return current


def get_next_rating_id():
    global rating_id_counter
    current = rating_id_counter
    rating_id_counter += 1
    return current


def reset_data():
    """Reset all data stores - used for testing"""
    global restaurants, dishes, users, orders, ratings, feedback
    global restaurant_id_counter, dish_id_counter, user_id_counter, order_id_counter, rating_id_counter
    
    restaurants.clear()
    dishes.clear()
    users.clear()
    orders.clear()
    ratings.clear()
    feedback.clear()
    
    restaurant_id_counter = 1
    dish_id_counter = 1
    user_id_counter = 1
    order_id_counter = 1
    rating_id_counter = 1
