class Parent:
    def parent(self):
        print("Parent 1")


class Child1(Parent):
    def child1(self):
        print("Child 1")


# Child class 2
class Child2(Parent):
    def child2(self):
        print("Child 2")


# Objects
obj1 = Child1()
obj2 = Child2()

# Method calls
obj1.parent()
obj1.child1()

obj2.parent()
obj2.child2()
