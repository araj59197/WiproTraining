import requests, json

url = "https://api.restful-api.dev/objects/ff8081819782e69e019be40e1e462ec1"

response = requests.delete(url)
print("Status Code:", response.status_code)

# Some DELETE responses may not return JSON
try:
    print(json.dumps(response.json(), indent=2))
except:
    print("Object deleted successfully")
