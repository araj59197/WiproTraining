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

# from __future__ import annotations
# from abc import ABC, abstractmethod
# from dataclasses import dataclass
# from typing import Dict, List, Iterator, Any, Optional
# import json
# import csv
# import time


# # -------------------- Exceptions --------------------
# class UniAppError(Exception):
#     pass


# class AlreadyExists(UniAppError):
#     pass


# class NotFound(UniAppError):
#     pass


# class BadInput(UniAppError):
#     pass


# # -------------------- Decorators --------------------
# def require_admin(fn):
#     def inner(self, *args, **kwargs):
#         if not self.admin_mode:
#             print("Access Denied: Admin privileges required")
#             return None
#         return fn(self, *args, **kwargs)

#     return inner


# def log_action(fn):
#     def inner(*args, **kwargs):
#         out = fn(*args, **kwargs)
#         print(f"[LOG] Method {fn.__name__}() executed successfully")
#         return out

#     return inner


# def measure(fn):
#     def inner(*args, **kwargs):
#         t0 = time.perf_counter()
#         out = fn(*args, **kwargs)
#         t1 = time.perf_counter()
#         print(f"[TIME] {fn.__name__} took {(t1 - t0):.6f} sec")
#         return out

#     return inner


# # -------------------- Descriptors --------------------
# class MarksRange:
#     """Allow only list of ints between 0 and 100."""

#     def __set_name__(self, owner, name):
#         self.key = "_" + name

#     def __get__(self, obj, objtype=None):
#         return getattr(obj, self.key)

#     def __set__(self, obj, value):
#         if not isinstance(value, list) or not value:
#             raise BadInput("Invalid Marks\nError: Marks should be between 0 and 100")
#         for m in value:
#             if not isinstance(m, int) or m < 0 or m > 100:
#                 raise BadInput(
#                     "Invalid Marks\nError: Marks should be between 0 and 100"
#                 )
#         setattr(obj, self.key, value)


# class ConfidentialPay:
#     """Salary readable only when faculty._can_view_salary == True."""

#     def __set_name__(self, owner, name):
#         self.key = "_" + name

#     def __get__(self, obj, objtype=None):
#         if not getattr(obj, "_can_view_salary", False):
#             raise PermissionError(
#                 "Unauthorized Salary Access\nAccess Denied: Salary is confidential"
#             )
#         return getattr(obj, self.key)

#     def __set__(self, obj, value):
#         if not isinstance(value, (int, float)) or value < 0:
#             raise BadInput("Salary must be a non-negative number")
#         setattr(obj, self.key, float(value))


# # -------------------- ABC: Person --------------------
# class Person(ABC):
#     created_count = 0  # class variable (tracks people created)

#     def __init__(self, uid: str, name: str, dept: str):
#         self.uid = uid.strip()
#         self.name = name.strip()
#         self.dept = dept.strip()
#         Person.created_count += 1

#     @abstractmethod
#     def get_details(self) -> str: ...

#     @abstractmethod
#     def calculate_performance(self) -> str: ...

#     def __del__(self):
#         # simple cleanup log hook (best-effort)
#         # avoid printing here (destructors can run at unpredictable times)
#         pass


# # -------------------- Inheritance --------------------
# # Hierarchical: Student and Faculty both inherit Person
# class Student(Person):
#     marks = MarksRange()

#     def __init__(self, sid: str, name: str, dept: str, sem: int, marks: List[int]):
#         super().__init__(sid, name, dept)
#         if not isinstance(sem, int) or sem <= 0:
#             raise BadInput("Semester must be a positive integer")
#         self.sem = sem
#         self.marks = marks
#         self.courses: List[str] = []

#     def enroll(self, course_code: str) -> None:
#         if course_code not in self.courses:
#             self.courses.append(course_code)

#     # Polymorphism: overriding
#     def get_details(self) -> str:
#         return (
#             "Student Details:\n"
#             "--------------------------------\n"
#             f"Name      : {self.name}\n"
#             f"Role      : Student\n"
#             f"Department: {self.dept}\n"
#         )

#     # Polymorphism: overriding
#     @log_action
#     @measure
#     def calculate_performance(self) -> str:
#         avg = round(self._avg(), 2)
#         grade = self._grade(avg)
#         return (
#             "Student Performance Report\n"
#             "--------------------------------\n"
#             f"Student Name : {self.name}\n"
#             f"Marks        : {self.marks}\n"
#             f"Average      : {avg}\n"
#             f"Grade        : {grade}\n"
#         )

#     def _avg(self) -> float:
#         # uses generator to produce marks (requirement)
#         total = 0
#         n = 0
#         for m in self._marks_stream():
#             total += m
#             n += 1
#         return total / n

#     def _marks_stream(self):
#         for m in self.marks:
#             yield m

#     @staticmethod
#     def _grade(avg: float) -> str:
#         if avg >= 90:
#             return "A+"
#         if avg >= 80:
#             return "A"
#         if avg >= 70:
#             return "B"
#         if avg >= 60:
#             return "C"
#         if avg >= 50:
#             return "D"
#         return "F"

#     # Operator overloading: compare students with >
#     def __gt__(self, other: "Student") -> bool:
#         if not isinstance(other, Student):
#             return NotImplemented
#         return self._avg() > other._avg()


# class Faculty(Person):
#     salary = ConfidentialPay()

#     def __init__(self, fid: str, name: str, dept: str, monthly_salary: float):
#         super().__init__(fid, name, dept)
#         self._can_view_salary = False
#         self.salary = monthly_salary
#         self.assigned: List[str] = []

#     def assign(self, course_code: str) -> None:
#         if course_code not in self.assigned:
#             self.assigned.append(course_code)

#     def get_details(self) -> str:
#         return (
#             "Faculty Details:\n"
#             "--------------------------------\n"
#             f"Name      : {self.name}\n"
#             f"Role      : Faculty\n"
#             f"Department: {self.dept}\n"
#         )

#     def calculate_performance(self) -> str:
#         return f"{self.name} performance: N/A"


# # Multilevel inheritance example: Person -> Student -> ResearchStudent
# class ResearchStudent(Student):
#     def __init__(
#         self, sid: str, name: str, dept: str, sem: int, marks: List[int], topic: str
#     ):
#         super().__init__(sid, name, dept, sem, marks)
#         self.topic = topic.strip()

#     def get_details(self) -> str:
#         base = super().get_details()
#         return base + f"Role      : Research Student\nTopic     : {self.topic}\n"


# # -------------------- Course + Operator Overloading --------------------
# class Course:
#     def __init__(self, code: str, title: str, credits: int, faculty_id: str):
#         self.code = code.strip()
#         self.title = title.strip()
#         if not isinstance(credits, int) or credits <= 0:
#             raise BadInput("Credits must be a positive integer")
#         self.credits = credits
#         self.faculty_id = faculty_id.strip()
#         self.roster: List[str] = []

#     def add_student(self, sid: str) -> None:
#         if sid not in self.roster:
#             self.roster.append(sid)

#     # + merges credits (returns int total)
#     def __add__(self, other: "Course") -> int:
#         if not isinstance(other, Course):
#             return NotImplemented
#         return self.credits + other.credits


# # -------------------- Department --------------------
# @dataclass
# class Department:
#     name: str
#     course_codes: List[str]


# # -------------------- Iterator for courses --------------------
# class CourseWalk:
#     def __init__(self, course_list: List[Course]):
#         self._data = course_list
#         self._pos = 0

#     def __iter__(self) -> "CourseWalk":
#         return self

#     def __next__(self) -> Course:
#         if self._pos >= len(self._data):
#             raise StopIteration
#         item = self._data[self._pos]
#         self._pos += 1
#         return item


# # -------------------- Helper: Storage --------------------
# class Storage:
#     @staticmethod
#     def load_students(path: str) -> List[Dict[str, Any]]:
#         try:
#             with open(path, "r", encoding="utf-8") as f:
#                 data = json.load(f)
#             if not isinstance(data, list):
#                 raise BadInput("students.json must contain a list")
#             return data
#         except FileNotFoundError:
#             raise FileNotFoundError("Error: File not found")
#         except json.JSONDecodeError:
#             raise BadInput("Error: invalid JSON format")

#     @staticmethod
#     def save_students(path: str, students: Dict[str, Student]) -> None:
#         payload = []
#         for s in students.values():
#             payload.append(
#                 {
#                     "id": s.uid,
#                     "name": s.name,
#                     "department": s.dept,
#                     "semester": s.sem,
#                     "marks": s.marks,
#                 }
#             )
#         with open(path, "w", encoding="utf-8") as f:
#             json.dump(payload, f, indent=2)
#         print(f"Student data successfully saved to {path}")

#     @staticmethod
#     def export_csv(path: str, students: Dict[str, Student]) -> None:
#         with open(path, "w", newline="", encoding="utf-8") as f:
#             w = csv.writer(f)
#             w.writerow(["ID", "Name", "Department", "Average", "Grade"])
#             for s in students.values():
#                 avg = round(sum(s.marks) / len(s.marks), 2)
#                 grade = Student._grade(avg)
#                 w.writerow([s.uid, s.name, s.dept, avg, grade])
#         print(f"CSV Report ({path}) created")


# # -------------------- Main System --------------------
# class UniSystem:
#     def __init__(self):
#         self.admin_mode = False
#         self.students: Dict[str, Student] = {}
#         self.faculty: Dict[str, Faculty] = {}
#         self.courses: Dict[str, Course] = {}
#         self.depts: Dict[str, Department] = {}

#     def set_admin(self):
#         pin = input("Enter admin PIN (demo: 1234): ").strip()
#         self.admin_mode = pin == "1234"
#         print("Admin login successful" if self.admin_mode else "Admin login failed")

#     def _ensure_dept(self, dept: str) -> None:
#         if dept not in self.depts:
#             self.depts[dept] = Department(dept, [])

#     @log_action
#     def add_student(self, s: Student) -> None:
#         if s.uid in self.students:
#             raise AlreadyExists("Error: Student ID already exists")
#         self.students[s.uid] = s
#         self._ensure_dept(s.dept)
#         print("Student Created Successfully")
#         print("--------------------------------")
#         print(f"ID        : {s.uid}")
#         print(f"Name      : {s.name}")
#         print(f"Department: {s.dept}")
#         print(f"Semester  : {s.sem}")

#     @require_admin
#     @log_action
#     def add_faculty(self, f: Faculty) -> None:
#         if f.uid in self.faculty:
#             raise AlreadyExists("Error: Faculty ID already exists")
#         self.faculty[f.uid] = f
#         self._ensure_dept(f.dept)
#         print("Faculty Created Successfully")
#         print("--------------------------------")
#         print(f"ID        : {f.uid}")
#         print(f"Name      : {f.name}")
#         print(f"Department: {f.dept}")

#     @require_admin
#     @log_action
#     def add_course(self, c: Course) -> None:
#         if c.code in self.courses:
#             raise AlreadyExists("Error: Course Code already exists")
#         if c.faculty_id not in self.faculty:
#             raise NotFound("Error: Faculty not found for given Faculty ID")
#         self.courses[c.code] = c
#         self.faculty[c.faculty_id].assign(c.code)

#         # link to department
#         self._ensure_dept(self.faculty[c.faculty_id].dept)
#         if c.code not in self.depts[self.faculty[c.faculty_id].dept].course_codes:
#             self.depts[self.faculty[c.faculty_id].dept].course_codes.append(c.code)

#         print("Course Added Successfully")
#         print("--------------------------------")
#         print(f"Course Code : {c.code}")
#         print(f"Course Name : {c.title}")
#         print(f"Credits     : {c.credits}")
#         print(f"Faculty     : {self.faculty[c.faculty_id].name}")

#     @log_action
#     def enroll_student(self, sid: str, course_code: str) -> None:
#         if sid not in self.students:
#             raise NotFound("Error: Student not found")
#         if course_code not in self.courses:
#             raise NotFound("Error: Course not found")
#         self.students[sid].enroll(course_code)
#         self.courses[course_code].add_student(sid)

#         print("Enrollment Successful")
#         print("--------------------------------")
#         print(f"Student Name : {self.students[sid].name}")
#         print(f"Course       : {self.courses[course_code].title}")

#     def compare(self, sid1: str, sid2: str) -> None:
#         if sid1 not in self.students or sid2 not in self.students:
#             raise NotFound("Error: Student not found")
#         s1, s2 = self.students[sid1], self.students[sid2]
#         print("Compare Two Students (> operator)")
#         print("Comparing Students Performance")
#         print("--------------------------------")
#         print(f"{s1.name} > {s2.name} : {s1 > s2}")

#     def merge_credits(self, c1: str, c2: str) -> None:
#         if c1 not in self.courses or c2 not in self.courses:
#             raise NotFound("Error: Course not found")
#         total = self.courses[c1] + self.courses[c2]
#         print("Merge Course Credits (+ operator)")
#         print(f"Total Credits After Merge : {total}")

#     def details_demo(self, sid: str, fid: str) -> None:
#         if sid not in self.students or fid not in self.faculty:
#             raise NotFound("Error: Student/Faculty not found")
#         print(self.students[sid].get_details())
#         print(self.faculty[fid].get_details())

#     def salary_demo(self, fid: str) -> None:
#         if fid not in self.faculty:
#             raise NotFound("Error: Faculty not found")
#         f = self.faculty[fid]
#         f._can_view_salary = self.admin_mode
#         try:
#             print(f"Salary for {f.name}: {f.salary}")
#         except PermissionError as e:
#             print(str(e))
#         finally:
#             f._can_view_salary = False

#     # Generator: yield student records batch-wise
#     def student_batches(self, chunk: int = 2):
#         keys = list(self.students.keys())
#         for i in range(0, len(keys), chunk):
#             group = keys[i : i + chunk]
#             yield [self.students[k] for k in group]

#     # Iterator: course traversal
#     def course_iterator(self) -> Iterator[Course]:
#         return CourseWalk(list(self.courses.values()))

#     def load_students_json(self, path: str):
#         data = Storage.load_students(path)
#         for item in data:
#             try:
#                 s = Student(
#                     item["id"],
#                     item["name"],
#                     item["department"],
#                     int(item["semester"]),
#                     [int(x) for x in item["marks"]],
#                 )
#                 self.add_student(s)
#             except AlreadyExists as e:
#                 print(str(e))
#             except Exception as e:
#                 print(f"Error: invalid data in JSON record -> {e}")

#     def save_students_json(self, path: str):
#         Storage.save_students(path, self.students)

#     def export_students_csv(self, path: str):
#         Storage.export_csv(path, self.students)


# # -------------------- Menu --------------------
# def run_app():
#     app = UniSystem()

#     menu = """
# 1 -> Add Student
# 2 -> Add Faculty
# 3 -> Add Course
# 4 -> Enroll Student to Course
# 5 -> Calculate Student Performance
# 6 -> Compare Two Students
# 7 -> Generate Reports
# 8 -> Load Students From JSON
# 9 -> Polymorphism Demo
# 10 -> Merge Course Credits
# 11 -> Salary Access Demo
# 12 -> Iterator/Generator Demo
# 13 -> Admin Login
# 14 -> Exit
# """

#     while True:
#         try:
#             print(menu)
#             ch = input("Enter choice: ").strip()

#             if ch == "1":
#                 sid = input("Student ID: ").strip()
#                 nm = input("Student Name: ").strip()
#                 dp = input("Department: ").strip()
#                 sm = int(input("Semester: ").strip())
#                 mk = [
#                     int(x)
#                     for x in input("Marks (5 subjects separated by space): ").split()
#                 ]
#                 app.add_student(Student(sid, nm, dp, sm, mk))

#             elif ch == "2":
#                 fid = input("Faculty ID: ").strip()
#                 nm = input("Faculty Name: ").strip()
#                 dp = input("Department: ").strip()
#                 sal = float(input("Monthly Salary: ").strip())
#                 app.add_faculty(Faculty(fid, nm, dp, sal))

#             elif ch == "3":
#                 code = input("Course Code: ").strip()
#                 title = input("Course Name: ").strip()
#                 credits = int(input("Credits: ").strip())
#                 fid = input("Faculty ID: ").strip()
#                 app.add_course(Course(code, title, credits, fid))

#             elif ch == "4":
#                 sid = input("Student ID: ").strip()
#                 code = input("Course Code: ").strip()
#                 app.enroll_student(sid, code)

#             elif ch == "5":
#                 sid = input("Student ID: ").strip()
#                 if sid not in app.students:
#                     raise NotFound("Error: Student not found")
#                 print(app.students[sid].calculate_performance())

#             elif ch == "6":
#                 s1 = input("Student ID 1: ").strip()
#                 s2 = input("Student ID 2: ").strip()
#                 app.compare(s1, s2)

#             elif ch == "7":
#                 csv_path = input("CSV path (e.g., students_report.csv): ").strip()
#                 json_path = input("JSON path (e.g., students.json): ").strip()
#                 app.export_students_csv(csv_path)
#                 app.save_students_json(json_path)

#             elif ch == "8":
#                 path = input("JSON file path (e.g., students.json): ").strip()
#                 app.load_students_json(path)

#             elif ch == "9":
#                 sid = input("Student ID: ").strip()
#                 fid = input("Faculty ID: ").strip()
#                 app.details_demo(sid, fid)

#             elif ch == "10":
#                 c1 = input("Course Code 1: ").strip()
#                 c2 = input("Course Code 2: ").strip()
#                 app.merge_credits(c1, c2)

#             elif ch == "11":
#                 fid = input("Faculty ID: ").strip()
#                 app.salary_demo(fid)

#             elif ch == "12":
#                 print("Student Record Generator")
#                 print("Fetching Student Records...")
#                 print("--------------------------------")
#                 for batch in app.student_batches(chunk=2):
#                     for s in batch:
#                         print(f"{s.uid} - {s.name}")

#                 print("\nCourse Iterator")
#                 print("--------------------------------")
#                 for c in app.course_iterator():
#                     print(f"{c.code} - {c.title} ({c.credits} credits)")

#             elif ch == "13":
#                 app.set_admin()

#             elif ch == "14":
#                 print("Thank you for using Smart University Management System")
#                 break

#             else:
#                 print("Invalid choice. Try again.")

#         except UniAppError as e:
#             print(str(e))
#         except FileNotFoundError as e:
#             print(str(e))
#         except ValueError:
#             print("Error: Invalid number entered")
#         except Exception as e:
#             print(f"Unexpected error: {e}")


# if __name__ == "__main__":
#     run_app()


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
