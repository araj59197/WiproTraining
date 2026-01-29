# Goal: Create an Employee class where 'salary' is strictly managed.
# We want to forbid negative salaries using a specialized helper class (Descriptor).

# This class acts as a "Guard" or "Validator" for the salary.
class PositiveNumber:

    def __set_name__(self, owner, name):

        self.private_name = "_" + name  

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        print(f"--> Checking if {value} is valid...") 
        
        if not isinstance(value, (int, float)):
            raise TypeError("Salary must be a number (integer or decimal)")
        
        if value < 0:
            raise ValueError("Error: Salary cannot be negative!")
        
        setattr(instance, self.private_name, value)
        print("    Valid! Saved.")


class Employee:
    salary = PositiveNumber()

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary  

if __name__ == "__main__":
    
    print("\n--- Test 1: Creating Alice (Valid Salary) ---")
    try:
        emp1 = Employee("Alice", 50000)
        print(f"Result: {emp1.name} has a salary of {emp1.salary}")
    except Exception as e:
        print(f"Something went wrong: {e}")

    print("\n--- Test 2: Creating Bob (Invalid Negative Salary) ---")
    try:
        emp2 = Employee("Bob", -2000)
    except ValueError as e:
        print(f"Result: Stopped creation because: {e}")

    print("\n--- Test 3: Updating Alice's salary to negative ---")
    try:
        emp1.salary = -100
    except ValueError as e:
        print(f"Result: Update failed because: {e}")
