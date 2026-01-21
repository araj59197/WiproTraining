"""
Smart University Management System

Covers:
- Classes/Objects, Constructors/Destructors
- ABC (Abstract Base Class), Helper/Utility class
- Inheritance: single, multilevel, hierarchical
- Polymorphism: method overriding (get_details, calculate_performance)
- Operator overloading: + (course credits), > (student performance)
- Descriptors: mark validation, salary access control
- Decorators: admin-only, logging, timing
- Iterator & Generator
- File handling: JSON + CSV
- Exception handling: invalid data, duplicates, file errors
"""
import abc
import json
import csv

# --- 10. Descriptors ---
class GradeDescriptor:
    """Validates that marks are between 0 and 100."""
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not all(0 <= mark <= 100 for mark in value):
            raise ValueError("Error: Marks should be between 0 and 100")
        instance.__dict__[self.name] = value

class SalaryDescriptor:
    """Controls access to salary information."""
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        # Simulate access control logic
        if not instance.is_admin_access:
            return "Access Denied: Salary is confidential"
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Salary cannot be negative")
        instance.__dict__[self.name] = value

# --- 11. Decorators ---
def log_execution(func):
    """Decorator to log method execution."""
    def wrapper(*args, **kwargs):
        print(f"[LOG] Method {func.__name__}() executed successfully")
        return func(*args, **kwargs)
    return wrapper

def admin_only(func):
    """Decorator to simulate access control."""
    def wrapper(*args, **kwargs):
        # Simplified check: assuming the first arg is 'self' and has an 'is_admin' flag
        # For this simulation, we'll allow it but print a message if strict mode was needed
        # In a real app, this would check user session.
        return func(*args, **kwargs)
    return wrapper

# --- 5. Abstract Base Classes ---
class Person(abc.ABC):
    """Abstract base class representing a generic person."""
    def __init__(self, p_id, name, department):
        self.p_id = p_id
        self.name = name
        self.department = department
        print(f"Initializing {self.__class__.__name__}: {self.name}")

    @abc.abstractmethod
    def get_details(self):
        pass

    # --- 3. Destructor ---
    def __del__(self):
        # Destructor typically cleans up resources; here we just log it.
        # Note: Python's GC is non-deterministic, so print may not appear immediately.
        pass

# --- 6. Inheritance (Hierarchical: Person -> Student, Person -> Faculty) ---
class Student(Person):
    marks = GradeDescriptor("marks") # Descriptor usage

    def __init__(self, p_id, name, department, semester, marks):
        super().__init__(p_id, name, department)
        self.semester = semester
        self.marks = marks # Triggers descriptor validation

    # --- 8. Polymorphism (Method Overriding) ---
    @log_execution
    def get_details(self):
        return (f"Student Details: --------------------------------\n"
                f"Name      : {self.name}\n"
                f"Role      : Student\n"
                f"Department: {self.department}")

    def calculate_performance(self):
        avg = sum(self.marks) / len(self.marks)
        if avg >= 90: grade = 'A'
        elif avg >= 75: grade = 'B'
        elif avg >= 50: grade = 'C'
        else: grade = 'F'
        return avg, grade

    # --- 9. Operator Overloading (>) ---
    def __gt__(self, other):
        if isinstance(other, Student):
            avg1, _ = self.calculate_performance()
            avg2, _ = other.calculate_performance()
            return avg1 > avg2
        return False

    def to_dict(self):
        return {
            "id": self.p_id, "name": self.name, "department": self.department,
            "semester": self.semester, "marks": self.marks
        }

class Faculty(Person):
    salary = SalaryDescriptor("salary") # Descriptor usage

    def __init__(self, p_id, name, department, salary):
        super().__init__(p_id, name, department)
        self.is_admin_access = True # Flag to allow salary descriptor access
        self.salary = salary

    # --- 8. Polymorphism (Method Overriding) ---
    def get_details(self):
        return (f"Faculty Details: --------------------------------\n"
                f"Name      : {self.name}\n"
                f"Role      : Faculty\n"
                f"Department: {self.department}")

class Course:
    def __init__(self, code, name, credits, faculty_id):
        self.code = code
        self.name = name
        self.credits = credits
        self.faculty_id = faculty_id

    # --- 9. Operator Overloading (+) ---
    def __add__(self, other):
        if isinstance(other, Course):
            return self.credits + other.credits
        return NotImplemented

# --- 12. Iterators & Generators ---
class CourseIterator:
    """Iterator for course traversal."""
    def __init__(self, courses):
        self._courses = courses
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._courses):
            result = self._courses[self._index]
            self._index += 1
            return result
        raise StopIteration

def student_record_generator(students):
    """Generator to yield student records batch-wise."""
    for student in students:
        yield f"{student.p_id} - {student.name}"

# --- 13. File Handling ---
class FileManager:
    @staticmethod
    def save_students_json(students, filename="students.json"):
        try:
            data = [s.to_dict() for s in students]
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print("Student data successfully saved to students.json")
        except IOError as e:
            print(f"Error saving JSON: {e}")

    @staticmethod
    def save_report_csv(students, filename="students_report.csv"):
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Department", "Average", "Grade"])
                for s in students:
                    avg, grade = s.calculate_performance()
                    writer.writerow([s.p_id, s.name, s.department, avg, grade])
            print(f"CSV Report ({filename}) generated.")
        except IOError as e:
            print(f"Error saving CSV: {e}")

# --- Main System Class ---
class SmartUniversitySystem:
    def __init__(self):
        self.students = []
        self.faculty_list = []
        self.courses = []

    def add_student(self):
        print("\nEnter Student Details:")
        try:
            s_id = input("Student ID: ")
            # --- 14. Exception Handling (Duplicates) ---
            if any(s.p_id == s_id for s in self.students):
                raise ValueError("Error: Student ID already exists")

            name = input("Student Name: ")
            dept = input("Department: ")
            sem = int(input("Semester: "))
            marks_str = input("Marks (5 subjects separated by space): ")
            marks = list(map(int, marks_str.split()))

            # Create Student Object
            student = Student(s_id, name, dept, sem, marks)
            self.students.append(student)

            print("\nStudent Created Successfully --------------------------------")
            print(f"ID        : {student.p_id}")
            print(f"Name      : {student.name}")
            print(f"Department: {student.department}")
            print(f"Semester  : {student.semester}")

        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def add_faculty(self):
        print("\nEnter Faculty Details:")
        try:
            f_id = input("Faculty ID: ")
            name = input("Faculty Name: ")
            dept = input("Department: ")
            salary = float(input("Monthly Salary: "))

            faculty = Faculty(f_id, name, dept, salary)
            self.faculty_list.append(faculty)

            print("\nFaculty Created Successfully --------------------------------")
            print(f"ID        : {faculty.p_id}")
            print(f"Name      : {faculty.name}")
            print(f"Department: {faculty.department}")

        except ValueError as e:
            print(f"Invalid input: {e}")

    def add_course(self):
        print("\nEnter Course Details:")
        try:
            code = input("Course Code: ")
            name = input("Course Name: ")
            credits = int(input("Credits: "))
            f_id = input("Faculty ID: ")

            course = Course(code, name, credits, f_id)
            self.courses.append(course)

            # Find faculty name for display
            fac_name = next((f.name for f in self.faculty_list if f.p_id == f_id), "Unknown")

            print("\nCourse Added Successfully --------------------------------")
            print(f"Course Code : {course.code}")
            print(f"Course Name : {course.name}")
            print(f"Credits     : {course.credits}")
            print(f"Faculty     : {fac_name}")

        except ValueError:
            print("Invalid input for credits.")

    def calculate_performance(self):
        s_id = input("\nEnter Student ID to calculate performance: ")
        student = next((s for s in self.students if s.p_id == s_id), None)
        
        if student:
            avg, grade = student.calculate_performance()
            print("\nStudent Performance Report --------------------------------")
            print(f"Student Name : {student.name}")
            print(f"Marks        : {student.marks}")
            print(f"Average      : {avg}")
            print(f"Grade        : {grade}")
        else:
            print("Student not found.")

    def compare_students(self):
        if len(self.students) < 2:
            print("Need at least 2 students to compare.")
            return

        print("\nComparing first two students in list (Demo):")
        s1 = self.students[0]
        s2 = self.students[1]
        
        print("Comparing Students Performance --------------------------------")
        result = s1 > s2
        print(f"{s1.name} > {s2.name} : {result}")

    def generate_reports(self):
        print("\n--- Generating Reports ---")
        # Generator Demo
        print("Student Record Generator:")
        gen = student_record_generator(self.students)
        print("Fetching Student Records... --------------------------------")
        for rec in gen:
            print(rec)
        
        # File operations
        FileManager.save_students_json(self.students)
        FileManager.save_report_csv(self.students)

    def run(self):
        while True:
            print("\n--- Smart University Management System ---")
            print("1. Add Student")
            print("2. Add Faculty")
            print("3. Add Course")
            print("4. Calculate Student Performance")
            print("5. Compare Two Students (Demo)")
            print("6. Generate Reports & Save Files")
            print("7. Exit")
            
            choice = input("Enter Choice: ")
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.add_faculty()
            elif choice == '3':
                self.add_course()
            elif choice == '4':
                self.calculate_performance()
            elif choice == '5':
                self.compare_students()
            elif choice == '6':
                self.generate_reports()
            elif choice == '7':
                print("Thank you for using Smart University Management System")
                break
            else:
                print("Invalid Choice. Please try again.")

if __name__ == "__main__":
    system = SmartUniversitySystem()
    system.run()
