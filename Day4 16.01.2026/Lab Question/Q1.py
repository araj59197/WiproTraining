# Create a class Student that:

# Has attributes name and roll_no

# Has a method display_details() to print student information


# Create at least two objects of the class and display their details
class Student:
    def __init__(self, name, roll_no):
        self.name = name
        self.roll_no = roll_no

    def display_details(self):
        print(f"Student Name: {self.name}")
        print(f"Roll Number: {self.roll_no}")
        print("-" * 30)


# Creating objects of Student class
student1 = Student("Aditya Kumar", 101)
student2 = Student("Priya Sharma", 102)

# Displaying details
print("Student Details:")
print("=" * 30)
student1.display_details()
student2.display_details()
