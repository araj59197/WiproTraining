# Topics: Class types, Introduction to Inheritance, Types of Inheritance
# 1. Create a base class Vehicle with a method start() 2. Create a derived class Car that inherits from Vehicle
# 3. Add a class variable to track the number of vehicles created
# 4. Demonstrate single inheritance and multilevel inheritance with appropriate classes
class Vehicle:
    vehicle_count = 0

    def __init__(self):
        Vehicle.vehicle_count += 1

    def start(self):
        print("Vehicle started")


class Car(Vehicle):
    def drive(self):
        print("Car is driving")


class ElectricCar(Car):
    def charge(self):
        print("Electric car is charging")


v1 = Vehicle()
c1 = Car()
e1 = ElectricCar()

v1.start()

c1.start()
c1.drive()

e1.start()
e1.drive()
e1.charge()

print("Total vehicles created:", Vehicle.vehicle_count)
