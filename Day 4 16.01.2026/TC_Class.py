class Student:
    def display(self):
        print("I am a student.")
s1 = Student()
s1.display()

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b
calc = Calculator()
print(calc.add(5, 3))
print(calc.subtract(10, 4))