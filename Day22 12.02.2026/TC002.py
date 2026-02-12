from pymongo import MongoClient

client=MongoClient("mongodb://localhost:27017/")
db=client["company_db"]
collection=db["employees"]

new_employee={
    "name":"Anurag",
    "department":"IT",
    "salary":75000

}
insert_result=collection.insert_one(new_employee)
print(f"\nInserted new employee with ID: {insert_result.inserted_id}")

print(f"\nDetails of inserted employee: {collection.find_one({"_id": insert_result.inserted_id})}")
