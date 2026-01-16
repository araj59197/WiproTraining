class Employee:
    def __init__(self, name):
        self.name = name
        print("Constructor called: Employee object created.")
    def __del__(self):
        print(f"Destructor called: Employee object '{self.name}' is being deleted.")
e1 = Employee("Alice")