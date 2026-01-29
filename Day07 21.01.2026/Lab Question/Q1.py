from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Aditya Raj", "email": "aditya@gmail.com"},
    {"id": 2, "name": "Bob", "email": "bob@gmail.com"}
]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400

    new_id = users[-1]['id'] + 1 if users else 1
    
    new_user = {
        "id": new_id,
        "name": data['name'],
        "email": data['email']
    }
    
    users.append(new_user)
    
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    # Validate JSON body
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400

    # Find user
    user = next((u for u in users if u['id'] == user_id), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update fields
    user['name'] = data['name']
    user['email'] = data['email']

    return jsonify(user), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)