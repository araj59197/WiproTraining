student = {"name": "Aditya", "age": 21, "course": "Python"}

print(student)
print(student["name"])
print(student.get("age"))


student["marks"] = 85
student["age"] = 22
print(student)
print(student["marks"])
print(student.get("age"))
student.pop("age")
print(student)
student.popitem()
print(student)

print(student.keys())
print(student.values())


for key in student:
    print(key, student[key])

if "name" in student:
    print("key exists")

employees = {
    101: {"name": "leena", "salary": 2000},
    102: {"name": "leena", "salary": 2000},
}

print(employees[101]["name"])
