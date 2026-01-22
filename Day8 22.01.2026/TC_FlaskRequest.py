import requests

geturl = "http://127.0.0.1:5000/users"

headers={
    "Accept":"application/json",
    "User-Agent":"Python-Requests-Client"

}

response = requests.get(geturl, headers=headers,timeout=10)

print("get status code", response.status_code)
print(response.json())


posturl = "http://127.0.0.1:5000/users"

body1 = {
    "name": "leena"
}

r1 = requests.post(posturl, json=body1)
print("post status code", r1.status_code)
print(r1.json())

puturl = "http://127.0.0.1:5000/users/1"
body2 = {
    "name": "leena Kumari",
    "email": "leena_kumari@gmail.com"
}
r2 = requests.put(puturl, json=body2)
print("put status code", r2.status_code)
print(r2.json())

patchurl = "http://127.0.0.1:5000/users/1"
body3 = {
    "email": "leena_patch@gmail.com"
}
r3 = requests.patch(patchurl, json=body3)
print("patch status code", r3.status_code)
print(r3.json())
