from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample Data
movies = [
    {
        "id": 101,
        "movie_name": "Interstellar",
        "language": "English",
        "duration": "2h 49m",
        "price": 250,
    },
    {
        "id": 102,
        "movie_name": "Inception",
        "language": "English",
        "duration": "2h 28m",
        "price": 220,
    },
]

bookings = []


# Helper function to find movie by ID
def find_movie(movie_id):
    return next((movie for movie in movies if movie["id"] == movie_id), None)


@app.route("/api/movies", methods=["GET"])
def get_movies():
    return jsonify(movies), 200


@app.route("/api/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = find_movie(movie_id)
    if movie:
        return jsonify(movie), 200
    return jsonify({"error": "Movie not found"}), 404


@app.route("/api/movies", methods=["POST"])
def add_movie():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    new_id = movies[-1]["id"] + 1 if movies else 101
    new_movie = {
        "id": new_id,
        "movie_name": data.get("movie_name"),
        "language": data.get("language"),
        "duration": data.get("duration"),
        "price": data.get("price"),
    }
    movies.append(new_movie)
    return jsonify(new_movie), 201


@app.route("/api/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    movie = find_movie(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    data = request.get_json()
    movie["movie_name"] = data.get("movie_name", movie["movie_name"])
    movie["language"] = data.get("language", movie["language"])
    movie["duration"] = data.get("duration", movie["duration"])
    movie["price"] = data.get("price", movie["price"])

    return jsonify(movie), 200


@app.route("/api/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    movie = find_movie(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    movies.remove(movie)
    return jsonify({"message": "Movie deleted successfully"}), 200


@app.route("/api/bookings", methods=["POST"])
def book_ticket():
    data = request.get_json()
    movie_id = data.get("movie_id")
    seats = data.get("seats")

    movie = find_movie(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    if not seats or seats <= 0:
        return jsonify({"error": "Invalid number of seats"}), 400

    booking = {
        "booking_id": len(bookings) + 1,
        "movie_id": movie_id,
        "movie_name": movie["movie_name"],
        "seats": seats,
        "total_price": movie["price"] * seats,
    }
    bookings.append(booking)
    return jsonify(booking), 201


if __name__ == "__main__":
    app.run(debug=True, port=5001)
