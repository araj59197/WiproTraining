# """
# Smart University Management System

# Covers:
# - Classes/Objects, Constructors/Destructors
# - ABC (Abstract Base Class), Helper/Utility class
# - Inheritance: single, multilevel, hierarchical
# - Polymorphism: method overriding (get_details, calculate_performance)
# - Operator overloading: + (course credits), > (student performance)
# - Descriptors: mark validation, salary access control
# - Decorators: admin-only, logging, timing
# - Iterator & Generator
# - File handling: JSON + CSV
# - Exception handling: invalid data, duplicates, file errors
# """

import abc
import json
import csv
import os
from datetime import datetime


# ---------------- Descriptors ----------------
class GradeDescriptor:
    """Validates that marks are between 0 and 100."""

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, list) or len(value) == 0:
            raise ValueError("Error: Marks must be a non-empty list.")
        if not all(isinstance(mark, (int, float)) for mark in value):
            raise ValueError("Error: Marks must be numbers.")
        if not all(0 <= mark <= 100 for mark in value):
            raise ValueError("Error: Marks should be between 0 and 100.")
        instance.__dict__[self.name] = value


class SalaryDescriptor:
    """Controls access to salary information."""

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not getattr(instance, "is_admin_access", False):
            return "Access Denied: Salary is confidential"
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Salary must be a number")
        if value < 0:
            raise ValueError("Salary cannot be negative")
        instance.__dict__[self.name] = value


# ---------------- Decorators ----------------
def log_execution(func):
    """Decorator to log method execution."""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[LOG] Method {func.__name__}() executed successfully")
        return result

    return wrapper


def admin_only(func):
    """Decorator placeholder for admin-only actions."""

    def wrapper(*args, **kwargs):
        # In a real system, you'd check session/user role here.
        return func(*args, **kwargs)

    return wrapper


# ---------------- Abstract Base Class ----------------
class Person(abc.ABC):
    """Abstract base class representing a generic person."""

    def __init__(self, p_id, name, department):
        self.p_id = str(p_id).strip()
        self.name = name.strip()
        self.department = department.strip()
        print(f"Initializing {self.__class__.__name__}: {self.name}")

    @abc.abstractmethod
    def get_details(self):
        pass

    def __del__(self):
        # Non-deterministic in Python, so kept empty intentionally.
        pass


# ---------------- Inheritance (Hierarchical) ----------------
class Student(Person):
    marks = GradeDescriptor("marks")

    def __init__(self, p_id, name, department, semester, marks):
        super().__init__(p_id, name, department)
        self.semester = int(semester)
        self.marks = marks

    @log_execution
    def get_details(self):
        return (
            "Student Details: --------------------------------\n"
            f"ID        : {self.p_id}\n"
            f"Name      : {self.name}\n"
            f"Role      : Student\n"
            f"Department: {self.department}\n"
            f"Semester  : {self.semester}"
        )

    def calculate_performance(self):
        if not self.marks:
            return 0.0, "F"
        avg = sum(self.marks) / len(self.marks)
        if avg >= 90:
            grade = "A"
        elif avg >= 75:
            grade = "B"
        elif avg >= 50:
            grade = "C"
        else:
            grade = "F"
        return avg, grade

    def __gt__(self, other):
        if isinstance(other, Student):
            avg1, _ = self.calculate_performance()
            avg2, _ = other.calculate_performance()
            return avg1 > avg2
        return False

    def to_dict(self):
        return {
            "id": self.p_id,
            "name": self.name,
            "department": self.department,
            "semester": self.semester,
            "marks": self.marks,
        }


class Faculty(Person):
    salary = SalaryDescriptor("salary")

    def __init__(self, p_id, name, department, salary):
        super().__init__(p_id, name, department)
        self.is_admin_access = True
        self.salary = float(salary)

    def get_details(self):
        return (
            "Faculty Details: --------------------------------\n"
            f"ID        : {self.p_id}\n"
            f"Name      : {self.name}\n"
            f"Role      : Faculty\n"
            f"Department: {self.department}\n"
            f"Salary    : {self.salary}"
        )


# ---------------- Course + Operator Overloading ----------------
class Course:
    def __init__(self, code, name, credits, faculty_id):
        self.code = code.strip()
        self.name = name.strip()
        self.credits = int(credits)
        self.faculty_id = str(faculty_id).strip()

    def __add__(self, other):
        if isinstance(other, Course):
            return self.credits + other.credits
        return NotImplemented


# ---------------- Iterator & Generator ----------------
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
    """Generator to yield student records."""
    for student in students:
        yield f"{student.p_id} - {student.name}"


# ---------------- File Handling (SAVE + LOAD) ----------------
class FileManager:
    @staticmethod
    def save_students_json(students, filename="students.json"):
        try:
            data = [s.to_dict() for s in students]
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"Student JSON saved: {os.path.abspath(filename)}")
        except IOError as e:
            print(f"Error saving JSON: {e}")

    @staticmethod
    def load_students_json(filename="students.json"):
        try:
            if not os.path.exists(filename):
                return []
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            students = []
            for item in data:
                students.append(
                    Student(
                        item["id"],
                        item["name"],
                        item["department"],
                        item["semester"],
                        item["marks"],
                    )
                )
            return students
        except (IOError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            print(f"Error loading students from JSON: {e}")
            return []

    @staticmethod
    def save_report_csv(students, filename="students_report.csv"):
        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["Generated On", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                )
                writer.writerow([])
                writer.writerow(
                    ["ID", "Name", "Department", "Semester", "Average", "Grade"]
                )
                for s in students:
                    avg, grade = s.calculate_performance()
                    writer.writerow(
                        [s.p_id, s.name, s.department, s.semester, round(avg, 2), grade]
                    )
            print(f"CSV report saved: {os.path.abspath(filename)}")
        except IOError as e:
            print(f"Error saving CSV: {e}")


# ---------------- Main System ----------------
class SmartUniversitySystem:
    def __init__(self):
        self.students = FileManager.load_students_json("students.json")
        self.faculty_list = []
        self.courses = []
        print(f"Loaded students: {len(self.students)}")

    def add_student(self):
        print("\nEnter Student Details:")
        try:
            s_id = input("Student ID: ").strip()
            if not s_id:
                raise ValueError("Student ID cannot be empty.")

            if any(s.p_id == s_id for s in self.students):
                raise ValueError("Error: Student ID already exists")

            name = input("Student Name: ").strip()
            dept = input("Department: ").strip()
            sem = int(input("Semester: ").strip())

            marks_str = input("Marks (5 subjects separated by space): ").strip()
            marks = list(map(int, marks_str.split()))

            student = Student(s_id, name, dept, sem, marks)
            self.students.append(student)

            # Auto-save so you don't lose data after restart
            FileManager.save_students_json(self.students, "students.json")

            print("\nStudent Created Successfully --------------------------------")
            print(student.get_details())

        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def add_faculty(self):
        print("\nEnter Faculty Details:")
        try:
            f_id = input("Faculty ID: ").strip()
            name = input("Faculty Name: ").strip()
            dept = input("Department: ").strip()
            salary = float(input("Monthly Salary: ").strip())

            faculty = Faculty(f_id, name, dept, salary)
            self.faculty_list.append(faculty)

            print("\nFaculty Created Successfully --------------------------------")
            print(faculty.get_details())

        except ValueError as e:
            print(f"Invalid input: {e}")

    def add_course(self):
        print("\nEnter Course Details:")
        try:
            code = input("Course Code: ").strip()
            name = input("Course Name: ").strip()
            credits = int(input("Credits: ").strip())
            f_id = input("Faculty ID: ").strip()

            course = Course(code, name, credits, f_id)
            self.courses.append(course)

            fac_name = next(
                (f.name for f in self.faculty_list if f.p_id == f_id), "Unknown"
            )

            print("\nCourse Added Successfully --------------------------------")
            print(f"Course Code : {course.code}")
            print(f"Course Name : {course.name}")
            print(f"Credits     : {course.credits}")
            print(f"Faculty     : {fac_name}")

        except ValueError:
            print("Invalid input for credits.")

    def calculate_student_performance(self):
        s_id = input("\nEnter Student ID to calculate performance: ").strip()
        student = next((s for s in self.students if s.p_id == s_id), None)

        if student:
            avg, grade = student.calculate_performance()
            print("\nStudent Performance Report --------------------------------")
            print(f"Student Name : {student.name}")
            print(f"Marks        : {student.marks}")
            print(f"Average      : {round(avg, 2)}")
            print(f"Grade        : {grade}")
        else:
            print("Student not found.")

    def compare_students(self):
        # Needs at least 2 students (loaded from JSON OR added now)
        if len(self.students) < 2:
            print("Need at least 2 students to compare.")
            return

        print("\nComparing first two students in list")
        s1 = self.students[0]
        s2 = self.students[1]

        print("Comparing Students Performance --------------------------------")
        result = s1 > s2
        print(f"{s1.name} > {s2.name} : {result}")

    def generate_reports(self):
        print("\n--- Generating Reports ---")

        print("Student Record Generator:")
        print("Fetching Student Records... --------------------------------")
        for rec in student_record_generator(self.students):
            print(rec)

        FileManager.save_students_json(self.students, "students.json")
        FileManager.save_report_csv(self.students, "students_report.csv")

    def list_courses_using_iterator(self):
        if not self.courses:
            print("No courses added yet.")
            return
        print("\n--- Listing Courses (Iterator Demo) ---")
        for c in CourseIterator(self.courses):
            print(
                f"{c.code} | {c.name} | Credits: {c.credits} | FacultyID: {c.faculty_id}"
            )

    def run(self):
        while True:
            print("\n--- Smart University Management System ---")
            print("1. Add Student")
            print("2. Add Faculty")
            print("3. Add Course")
            print("4. Calculate Student Performance")
            print("5. Compare Two Students")
            print("6. Generate Reports & Save Files (JSON + CSV)")
            print("7. List Courses")
            print("8. Exit")

            choice = input("Enter Choice: ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.add_faculty()
            elif choice == "3":
                self.add_course()
            elif choice == "4":
                self.calculate_student_performance()
            elif choice == "5":
                self.compare_students()
            elif choice == "6":
                self.generate_reports()
            elif choice == "7":
                self.list_courses_using_iterator()
            elif choice == "8":
                print("Thank you for using Smart University Management System")
                break
            else:
                print("Invalid Choice. Please try again.")


if __name__ == "__main__":
    system = SmartUniversitySystem()
    system.run()
