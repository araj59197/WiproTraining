# Postman Testing Guide - Foodie App API

## Setup Postman

1. **Download Postman**: https://www.postman.com/downloads/
2. **Install and Open Postman**
3. **Create a New Collection**: "Foodie App API Tests"

---

## Base URL
```
http://localhost:5000
```

---

## 1. Restaurant Module Tests

### Test 1: Register Restaurant (Positive)

**Request:**
- **Method:** POST
- **URL:** `http://localhost:5000/api/v1/restaurants`
- **Headers:**
  - `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
    "name": "Food Hub",
    "category": "Indian",
    "location": "Mumbai",
    "contact": "1234567890",
    "images": ["image1.jpg", "image2.jpg"]
}
```

**Expected Response:**
- **Status Code:** 201 Created
- **Response Body:**
```json
{
    "id": 1,
    "name": "Food Hub",
    "category": "Indian",
    "location": "Mumbai",
    "contact": "1234567890",
    "images": ["image1.jpg", "image2.jpg"],
    "enabled": true,
    "approved": false
}
```

**Validation Points:**
- ✅ Status code is 201
- ✅ Response contains `id`
- ✅ `name` matches request
- ✅ `enabled` is true by default
- ✅ `approved` is false by default

---

### Test 2: Register Restaurant (Negative - Missing Fields)

**Request:**
- **Method:** POST
- **URL:** `http://localhost:5000/api/v1/restaurants`
- **Body:**
```json
{
    "name": "Incomplete Restaurant",
    "category": "Italian"
}
```

**Expected Response:**
- **Status Code:** 400 Bad Request
- **Response Body:**
```json
{
    "error": "Missing required field: location"
}
```

**Validation:**
- ✅ Status code is 400
- ✅ Error message is present

---

### Test 3: Register Duplicate Restaurant (Negative)

**Request:**
- **Method:** POST
- **URL:** `http://localhost:5000/api/v1/restaurants`
- **Body:** (Same as Test 1)
```json
{
    "name": "Food Hub",
    "category": "Indian",
    "location": "Mumbai",
    "contact": "1234567890"
}
```

**Expected Response:**
- **Status Code:** 409 Conflict
- **Response Body:**
```json
{
    "error": "Restaurant with this name already exists"
}
```

---

### Test 4: Update Restaurant (Positive)

**Request:**
- **Method:** PUT
- **URL:** `http://localhost:5000/api/v1/restaurants/1`
- **Body:**
```json
{
    "category": "Pan-Indian",
    "location": "Mumbai Central"
}
```

**Expected Response:**
- **Status Code:** 200 OK
- **Response Body:** Updated restaurant with new values

---

### Test 5: View Restaurant (Positive)

**Request:**
- **Method:** GET
- **URL:** `http://localhost:5000/api/v1/restaurants/1`

**Expected Response:**
- **Status Code:** 200 OK
- **Response Body:** Complete restaurant details

---

### Test 6: View Non-existent Restaurant (Negative)

**Request:**
- **Method:** GET
- **URL:** `http://localhost:5000/api/v1/restaurants/9999`

**Expected Response:**
- **Status Code:** 404 Not Found
- **Response Body:**
```json
{
    "error": "Restaurant not found"
}
```

---

### Test 7: Disable Restaurant

**Request:**
- **Method:** PUT
- **URL:** `http://localhost:5000/api/v1/restaurants/1/disable`

**Expected Response:**
- **Status Code:** 200 OK
- **Response Body:**
```json
{
    "message": "Restaurant disabled"
}
```

---

## 2. Dish Module Tests

### Test 8: Add Dish (Positive)

**Request:**
- **Method:** POST
- **URL:** `http://localhost:5000/api/v1/restaurants/1/dishes`
- **Body:**
```json
{
    "name": "Butter Chicken",
    "type": "Main Course",
    "price": 350,
    "available_time": "Lunch & Dinner",
    "image": "butter_chicken.jpg"
}
```

**Expected Response:**
- **Status Code:** 201 Created
- **Response Body:**
```json
{
    "id": 1,
    "restaurant_id": 1,
    "name": "Butter Chicken",
    "type": "Main Course",
    "price": 350,
    "available_time": "Lunch & Dinner",
    "image": "butter_chicken.jpg",
    "enabled": true
}
```

---

### Test 9: Update Dish

**Request:**
- **Method:** PUT
- **URL:** `http://localhost:5000/api/v1/dishes/1`
- **Body:**
```json
{
    "price": 380,
    "available_time": "All Day"
}
```

**Expected Response:**
- **Status Code:** 200 OK

---

### Test 10: Toggle Dish Status

**Request:**
- **Method:** PUT
- **URL:** `http://localhost:5000/api/v1/dishes/1/status`
- **Body:**
```json
{
    "enabled": false
}
```

**Expected Response:**
- **Status Code:** 200 OK
- **Response Body:**
```json
{
    "message": "Dish disabled"
}
```

---

### Test 11: Delete Dish

**Request:**
- **Method:** DELETE
- **URL:** `http://localhost:5000/api/v1/dishes/1`

**Expected Response:**
- **Status Code:** 200 OK
- **Response Body:**
```json
{
    "message": "Dish deleted"
}
```

---

## 3. User Module Tests

### Test 12: Register User (Positive)

**Request:**
- **Method:** POST
- **URL:** `http://localhost:5000/api/v1/users/register`
- **Body:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepass123"
}
```

**Expected Response:**
- **Status Code:** 201 Created
- **Response Body:**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
}
```

**Note:** Password should NOT be in response!

---

### Test 13: Register Duplicate User (Negative)

**Request:**
- **Method:** POST
- **URL:** `http://localhost:5000/api/v1/users/register`
- **Body:** (Same as Test 12)

**Expected Response:**
- **Status Code:** 409 Conflict
- **Response Body:**
```json
{
    "error": "User with this email already exists"
}
```

---

### Test 14: Search Restaurants

**Prerequisites:** Create and approve a restaurant first

**Request:**
- **Method:** GET
- **URL:** `http://localhost:5000/api/v1/restaurants/search?location=Mumbai`

**Expected Response:**
- **Status Code:** 200 OK
- **Response Body:** Array of restaurants matching criteria

**Other Search Examples:**
```
?name=Food
?location=Mumbai&category=Indian
?dish=chicken
?rating=4
```

---

### Test 15: Place Order (Positive)

**Request:**
- **Method:** POST
- **URL:** `http://localhost:5000/api/v1/orders`
- **Body:**
```json
{
    "user_id": 1,
    "restaurant_id": 1,
    "dishes": [
        {"dish_id": 1, "quantity": 2},
        {"dish_id": 2, "quantity": 1}
    ],
    "total": 750
}
```

**Expected Response:**
- **Status Code:** 201 Created
- **Response Body:**
```json
{
    "id": 1,
    "user_id": 1,
    "restaurant_id": 1,
    "dishes": [...],
    "status": "pending",
    "total": 750
}
```

---

### Test 16: Place Order (Negative - Invalid User)

**Request:**
- **Method:** POST
- **URL:** `http://localhost:5000/api/v1/orders`
- **Body:**
```json
{
    "user_id": 9999,
    "restaurant_id": 1,
    "dishes": []
}
```

**Expected Response:**
- **Status Code:** 400 Bad Request
- **Response Body:**
```json
{
    "error": "User not found"
}
```

---

### Test 17: Give Rating (Positive)

**Request:**
- **Method:** POST
- **URL:** `http://localhost:5000/api/v1/ratings`
- **Body:**
```json
{
    "order_id": 1,
    "rating": 4.5,
    "comment": "Great food and quick delivery!"
}
```

**Expected Response:**
- **Status Code:** 201 Created
- **Response Body:**
```json
{
    "id": 1,
    "order_id": 1,
    "rating": 4.5,
    "comment": "Great food and quick delivery!"
}
```

---

### Test 18: Give Rating (Negative - Invalid Rating)

**Request:**
- **Method:** POST
- **URL:** `http://localhost:5000/api/v1/ratings`
- **Body:**
```json
{
    "order_id": 1,
    "rating": 6
}
```

**Expected Response:**
- **Status Code:** 400 Bad Request
- **Response Body:**
```json
{
    "error": "Rating must be between 1 and 5"
}
```

---

## 4. Admin Module Tests

### Test 19: Approve Restaurant

**Request:**
- **Method:** PUT
- **URL:** `http://localhost:5000/api/v1/admin/restaurants/1/approve`

**Expected Response:**
- **Status Code:** 200 OK
- **Response Body:**
```json
{
    "message": "Restaurant approved"
}
```

---

### Test 20: View All Feedback

**Request:**
- **Method:** GET
- **URL:** `http://localhost:5000/api/v1/admin/feedback`

**Expected Response:**
- **Status Code:** 200 OK
- **Response Body:** Array of feedback entries

---

### Test 21: View All Orders

**Request:**
- **Method:** GET
- **URL:** `http://localhost:5000/api/v1/admin/orders`

**Expected Response:**
- **Status Code:** 200 OK
- **Response Body:** Array of all orders

---

## 5. Order Module Tests

### Test 22: View Orders by Restaurant

**Request:**
- **Method:** GET
- **URL:** `http://localhost:5000/api/v1/restaurants/1/orders`

**Expected Response:**
- **Status Code:** 200 OK
- **Response Body:** Array of orders for that restaurant

---

### Test 23: View Orders by User

**Request:**
- **Method:** GET
- **URL:** `http://localhost:5000/api/v1/users/1/orders`

**Expected Response:**
- **Status Code:** 200 OK
- **Response Body:** Array of orders for that user

---

## Testing Workflow in Postman

### Step-by-Step Testing Process:

**1. Create Collection**
- Click "New" → "Collection"
- Name it "Foodie App API"

**2. Add Requests**
- Click "Add request" in your collection
- Name each request (e.g., "Create Restaurant")
- Set method, URL, headers, and body

**3. Run Tests in Order:**

```
1. POST /api/v1/restaurants (Create restaurant)
2. GET /api/v1/restaurants/1 (View restaurant)
3. POST /api/v1/restaurants/1/dishes (Add dish)
4. POST /api/v1/users/register (Register user)
5. PUT /api/v1/admin/restaurants/1/approve (Approve restaurant)
6. GET /api/v1/restaurants/search?location=Mumbai (Search)
7. POST /api/v1/orders (Place order)
8. POST /api/v1/ratings (Give rating)
9. GET /api/v1/admin/feedback (View feedback)
10. GET /api/v1/users/1/orders (View user orders)
```

**4. Use Postman Tests Tab**

Add this to the "Tests" tab for automated validation:

```javascript
// Check status code
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

// Check response has id
pm.test("Response has id", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
});

// Check response time
pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

**5. Save Environment Variables**

Create environment for base URL:
- Variable: `base_url`
- Value: `http://localhost:5000`

Then use: `{{base_url}}/api/v1/restaurants`

---

## Quick Checklist

### Positive Scenarios
- [ ] Create restaurant with all fields
- [ ] View existing restaurant
- [ ] Update restaurant details
- [ ] Add dish to restaurant
- [ ] Register new user
- [ ] Place order
- [ ] Give rating
- [ ] Search restaurants

### Negative Scenarios
- [ ] Create restaurant with missing fields (400)
- [ ] Create duplicate restaurant (409)
- [ ] View non-existent restaurant (404)
- [ ] Update non-existent restaurant (404)
- [ ] Invalid rating value (400)
- [ ] Order with invalid user (400)
- [ ] Empty dishes in order (400)

### Status Code Validation
- [ ] 200 - Successful GET/PUT
- [ ] 201 - Successful POST (creation)
- [ ] 400 - Bad Request (invalid input)
- [ ] 404 - Not Found
- [ ] 409 - Conflict (duplicate)

---

## Tips for Postman Testing

1. **Save Requests**: Save each request in the collection for reuse
2. **Use Variables**: Store IDs from responses to use in subsequent requests
3. **Organize**: Group requests by module (Restaurant, Dish, User, etc.)
4. **Document**: Add descriptions to each request
5. **Test Scripts**: Add automated assertions in the Tests tab
6. **Run Collection**: Use Collection Runner to run all tests at once

---

**Happy Testing! 🚀**
