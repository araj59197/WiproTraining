# Topics: Introduction to Polymorphism, Polymorphism on Operators
# 1. Create a class Calculator that demonstrates method overriding
# 2. Create another class AdvancedCalculator that overrides a method from Calculator
# 3. Implement operator overloading by overloading the + operator to add two objects of a custom class
# 4. Demonstrate polymorphism using the same method name with different behaviors


class BasicCalculator:
    def operate(self, x, y):
        return x + y


class SmartCalculator(BasicCalculator):
    def operate(self, x, y):
        return x * y


class Point:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, other):
        return Point(self.a + other.a, self.b + other.b)

    def display(self):
        return f"Point({self.a}, {self.b})"


def perform_operation(calculator, x, y):
    print(calculator.__class__.__name__, "output:", calculator.operate(x, y))


base_calc = BasicCalculator()
smart_calc = SmartCalculator()

perform_operation(base_calc, 8, 4)
perform_operation(smart_calc, 8, 4)

p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = p1 + p2

print("p1:", p1.display())
print("p2:", p2.display())
print("p1 + p2:", p3.display())
