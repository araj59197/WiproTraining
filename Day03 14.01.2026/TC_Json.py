import json

# Sample data to be written to JSON file
data = {
    "name": "Aditya",
    "age": 21,
    "course": "Python",
    "Skills": ["Python", "Java", "C++"],
}

# Writing data to JSON file
with open("data.json", "w") as f:
    json.dump(data, f, indent=10)
