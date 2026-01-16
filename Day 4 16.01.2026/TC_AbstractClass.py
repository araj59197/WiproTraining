from abc import ABC, abstractmethod


class Shape(ABC):
    def display(self):
        print("normal method")
    @abstractmethod
    def area(self):
        pass

    # a = Shape()
    # a.area()  # This will raise an error because we cannot instantiate an abstract class


class Rectangle(Shape):
    def area1(self):
        print("area method implemented in Rectangle class")


r = Rectangle()
r.area()
r.display()
