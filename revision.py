import json

from flask import Flask, request, jsonify

# with open("Users.json", "r") as file:

#     users_data = json.load(file)

users_data = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.j@example.com",
        "role": "Admin",
        "active": "True",
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob.smith@example.com",
        "role": "User",
        "active": "True",
    },
    {
        "id": 3,
        "name": "Charlie Davis",
        "email": "charlie.d@example.com",
        "role": "User",
        "active": "False",
    },
    {
        "id": 4,
        "name": "Diana Prince",
        "email": "diana.p@example.com",
        "role": "Moderator",
        "active": "True",
    },
    {
        "id": 5,
        "name": "Ethan Hunt",
        "email": "ethan.h@example.com",
        "role": "User",
        "active": "True",
    },
]

app = Flask(__name__)

app.json.sort_keys = False


@app.route("/", methods=["GET"])
def health():

    try:

        return jsonify({"Status": "UP", "Status": "Flask server is running"}), 200

    except Exception as e:

        return jsonify({"Message": "Internal server errro", "error": str(e)}), 500


@app.route("/users", methods=["GET"])
def getUsers():

    try:

        print(request.headers)

        if not users_data or len(users_data) == 0:

            return jsonify({"message": "No users found"}), 200

        return (
            jsonify({"message": "Users fetched successfully", "data": users_data}),
            200,
        )

    except Exception as e:

        return jsonify({"message": "internal server error", "error": str(e)}), 500


if __name__ == "__main__":

    app.run("0.0.0.0", port=5001, debug=True)


import requests, json

server_url = "http://127.0.0.1:5001"
users_url = "http://127.0.0.1:5001/users"


customHeader = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Python-Requests-Client",
}


server_status = requests.get(server_url, headers=customHeader)
print(server_status.status_code)
print(server_status.json())

user_data = requests.get(users_url, customHeader)
print(user_data.status_code)
response_data = user_data.json()
print(response_data["data"])
print(response_data["message"])
try:
    with open("userdump.json", "w") as file:
        json.dump(response_data["data"], file, indent=4)

except Exception as e:
    print(f"error dumping data into file: {str(e)}")