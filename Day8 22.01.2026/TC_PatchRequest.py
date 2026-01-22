import requests, json

url = "https://api.restful-api.dev/objects"

body = {
    "name": "Test Product",
    "data": {
        "price": 1500
    }
}

response = requests.post(url, json=body)
print("Status Code:", response.status_code)
print(json.dumps(response.json(), indent=2))

new_id = response.json()["id"]
print("NEW ID:", new_id)

