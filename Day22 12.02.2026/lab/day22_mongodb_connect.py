import pymongo
from pymongo import MongoClient

def mongodb_operations():
    try:
        client = MongoClient('localhost', 27017)
        
        db = client['company_db']
        collection = db['employees']
        
        print("Connected to MongoDB successfully!")

        new_employee = {
            "name": "Aditya",
            "department": "IT",
            "salary": 75000
        }
        insert_result = collection.insert_one(new_employee)
        print(f"\nInserted new employee with ID: {insert_result.inserted_id}")

        print("\nEmployees in 'IT' department:")
        query = {"department": "IT"}
        it_employees = collection.find(query)
        
        count = 0
        for emp in it_employees:
            print(emp)
            count += 1
        
        if count == 0:
            print("No employees found in IT department.")

        employee_name_to_update = "Aditya"
        update_query = {"name": employee_name_to_update}
        new_values = {"$set": {"salary": 82500}}
        
        update_result = collection.update_one(update_query, new_values)
        
        print(f"\nUpdated salary for '{employee_name_to_update}'.")
        print(f"Matched count: {update_result.matched_count}, Modified count: {update_result.modified_count}")

        updated_emp = collection.find_one({"name": employee_name_to_update})
        if updated_emp:
            print("Updated Employee Record:", updated_emp)

    except Exception as e:
        print("An error occurred:", e)
    finally:
        if 'client' in locals():
            client.close()
            print("\nMongoDB connection closed.")

if __name__ == "__main__":
    mongodb_operations()