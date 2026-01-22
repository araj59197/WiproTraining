import requests
import json

geturl = "https://api.restful-api.dev/objects"

response = requests.get(geturl)
print("Status Code:", response.status_code)
print("\nFormatted Response:\n")

data = response.json()

for item in data:
    print(json.dumps(item, indent=2))
    print("-" * 50)


posturl = "https://api.restful-api.dev/objects"
body = {
    "name": "Apple MacBook Pro 16",
    "data": {
        "year": 2019,
        "price": 1849.99,
        "CPU model": "Intel Core i9",
        "Hard disk size": "1 TB",
    },
}

r1 = requests.post(posturl, json=body)
print("POST Status Code:", r1.status_code)
print("POST Response:", r1.json())
post_response = r1.json()

print("\nPOST Response Details:\n")
for key, value in post_response.items():
    print(f"{key}: {value}")
