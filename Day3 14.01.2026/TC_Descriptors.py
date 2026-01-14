#Descriptor: A descriptor is a special type of object in Python that customizes the behavior of attribute access.
# It allows you to define how attributes are retrieved, set, or deleted in a class.
class mydescriptor:
    def __get__(self, object, owner):
        print(f"Getting value from {object}")
        return object._x

    def __set__(self, object, value):
        print(f"Setting value to {value}")
        object._x = value


class test:
    x = mydescriptor()


t = test()
t.x = 10
print(t.x)
