from flask import Flask, request, jsonify

app = Flask(__name__)

users = [{"id": 1, "name": "Raja"}, {"id": 2, "name": "Rama"}]


@app.route("/", methods=["Get"])
def home():
    return "Welcome"


@app.route("/users", methods=["Get"])
def get_users():
    return jsonify(users)


@app.route("/users/<int:user_id>", methods=["Get"])
def get_user(user_id):

    for user in users:
        if user["id"] == user_id:
            return jsonify(user)
    return jsonify({"message": "user not found"}), 404


@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    newuser = {"id": len(users) + 1, "name": data.get("name")}
    users.append(newuser)
    return jsonify(newuser), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json

    if not data or "name" not in data:
        return jsonify({"message": "Name is required"}), 400

    for user in users:
        if user["id"] == user_id:
            user["name"] = data["name"]
            return jsonify(user), 200

    return jsonify({"message": "user not found"}), 404


@app.route("/users/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    data = request.json

    if not data:
        return jsonify({"message": "No data provided"}), 400

    for user in users:
        if user["id"] == user_id:
            if "name" in data:
                user["name"] = data["name"]
            return jsonify(user), 200

    return jsonify({"message": "user not found"}), 404


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return jsonify({"message": "User deleted"}), 204
    return jsonify({"message": "user not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
