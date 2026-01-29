# Example of a simple class
class student:
    name = "Aditya"
    age = 21


s1 = student()
print(s1.name)
print(s1.age)


# Example of a class with constructor
class employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age


e1 = employee("Ravi", 25)
print(e1.name)
print(e1.age)
