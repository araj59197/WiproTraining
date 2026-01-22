# import requests, json

# url = "https://api.restful-api.dev/objects/13"

# body = {
#     "name": "Apple MacBook Pro 16",
#     "data": {
#         "year": 2019,
#         "price": 2049.99,
#         "CPU model": "Intel Core i9",
#         "Hard disk size": "1 TB",
#         "color": "silver",
#     },
# }

# response = requests.put(url, json=body)
# print("Status Code:", response.status_code)
# print(json.dumps(response.json(), indent=2))


import requests, json

# Step 1: Create a new object via POST
posturl = "https://api.restful-api.dev/objects"
body = {
    "name": "Apple MacBook Pro 16",
    "data": {
        "year": 2019,
        "price": 2049.99,
        "CPU model": "Intel Core i9",
        "Hard disk size": "1 TB",
        "color": "silver",
    },
}

response = requests.post(posturl, json=body)
print("POST Status Code:", response.status_code)
post_data = response.json()
print(json.dumps(post_data, indent=2))

# Step 2: Get the new ID from POST response
new_id = post_data.get("id")
print(f"\nNew Object ID: {new_id}")

# Step 3: Use the new ID for PUT request
if new_id:
    put_url = f"https://api.restful-api.dev/objects/{new_id}"
    put_response = requests.put(put_url, json=body)
    print(f"\nPUT Status Code: {put_response.status_code}")
    print(json.dumps(put_response.json(), indent=2))
