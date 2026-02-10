# Foodie App - Flask REST API

A complete Flask REST API for a food delivery application with Restaurant, Dish, Admin, User, and Order management.

## Features

### Modules
- **Restaurant Module**: Register, update, disable, and view restaurants
- **Dish Module**: Add, update, toggle status, and delete dishes
- **Admin Module**: Approve/disable restaurants, view feedback and orders
- **User Module**: Register users, search restaurants, place orders, give ratings
- **Order Module**: View orders by restaurant or user

### Total Endpoints: 18 REST APIs

## Technology Stack
- **Backend**: Python Flask 3.0
- **Testing**: Pytest, Robot Framework
- **Data Storage**: In-memory (for demonstration)

## Project Structure
```
FoodieApp/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── data_store.py
│   ├── services/
│   │   └── validation.py
│   └── routes/
│       ├── restaurant_routes.py
│       ├── dish_routes.py
│       ├── admin_routes.py
│       ├── user_routes.py
│       └── order_routes.py
├── tests/
│   ├── test_restaurants.py
│   ├── test_users_orders.py
│   └── robot/
│       └── foodie_api_tests.robot
├── run.py
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Install Dependencies
```powershell
cd FoodieApp
pip install -r requirements.txt
```

### 2. Run the Flask Server
```powershell
python run.py
```

Server will start on http://localhost:5000

### 3. Test with Postman or curl

**Create Restaurant:**
```powershell
curl -X POST http://localhost:5000/api/v1/restaurants -H "Content-Type: application/json" -d "{\"name\":\"Food Hub\",\"category\":\"Indian\",\"location\":\"Mumbai\",\"contact\":\"1234567890\"}"
```

**Register User:**
```powershell
curl -X POST http://localhost:5000/api/v1/users/register -H "Content-Type: application/json" -d "{\"name\":\"John\",\"email\":\"john@example.com\",\"password\":\"pass123\"}"
```

**Search Restaurants:**
```powershell
curl "http://localhost:5000/api/v1/restaurants/search?location=Mumbai"
```

## Run Tests

### Pytest Tests
```powershell
python -m pytest tests/ -v
```

### Robot Framework Tests
```powershell
robot tests/robot/foodie_api_tests.robot
```

## API Endpoints

### Restaurant Module
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/restaurants` | Register restaurant |
| PUT | `/api/v1/restaurants/{id}` | Update restaurant |
| PUT | `/api/v1/restaurants/{id}/disable` | Disable restaurant |
| GET | `/api/v1/restaurants/{id}` | View restaurant |

### Dish Module
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/restaurants/{id}/dishes` | Add dish |
| PUT | `/api/v1/dishes/{id}` | Update dish |
| PUT | `/api/v1/dishes/{id}/status` | Enable/disable dish |
| DELETE | `/api/v1/dishes/{id}` | Delete dish |

### Admin Module
| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/api/v1/admin/restaurants/{id}/approve` | Approve restaurant |
| PUT | `/api/v1/admin/restaurants/{id}/disable` | Disable restaurant |
| GET | `/api/v1/admin/feedback` | View feedback |
| GET | `/api/v1/admin/orders` | View all orders |

### User Module
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/register` | Register user |
| GET | `/api/v1/restaurants/search` | Search restaurants |
| POST | `/api/v1/orders` | Place order |
| POST | `/api/v1/ratings` | Give rating |

###Order Module
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/restaurants/{id}/orders` | View restaurant orders |
| GET | `/api/v1/users/{id}/orders` | View user orders |

## Status Codes
- **200** OK - Successful GET/PUT/DELETE
- **201** Created - Successful POST
- **400** Bad Request - Invalid input
- **404** Not Found - Resource doesn't exist
- **409** Conflict - Duplicate entry

## Example Requests

### Create and Update Restaurant
```python
import requests

# Create
data = {"name": "My Restaurant", "category": "Italian", "location": "Delhi", "contact": "1234567890"}
response = requests.post("http://localhost:5000/api/v1/restaurants", json=data)
restaurant_id = response.json()['id']

# Update
update_data = {"category": "Pan-Italian"}
requests.put(f"http://localhost:5000/api/v1/restaurants/{restaurant_id}", json=update_data)
```

### Place Order Flow
```python
# 1. Register user
user_data = {"name": "Customer", "email": "customer@example.com", "password": "pass"}
user_response = requests.post("http://localhost:5000/api/v1/users/register", json=user_data)
user_id = user_response.json()['id']

# 2. Search restaurants
restaurants = requests.get("http://localhost:5000/api/v1/restaurants/search?location=Mumbai")

# 3. Place order
order_data = {"user_id": user_id, "restaurant_id": 1, "dishes": [{"dish_id": 1, "quantity": 2}]}
requests.post("http://localhost:5000/api/v1/orders", json=order_data)
```

## Notes
- This uses in-memory storage (data is lost on server restart)
- For production, integrate a real database (PostgreSQL, MongoDB, etc.)
- Passwords are stored in plain text (use hashing in production)
- No authentication/authorization implemented (add JWT for production)

## Author
Created for Wipro Pre-Skilling Training - Day 20
