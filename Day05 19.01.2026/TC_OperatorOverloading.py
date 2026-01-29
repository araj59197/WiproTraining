class Box1:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return self.value + other.value

b1 = Box1(50)
b2 = Box1(30)

print(b1 + b2)   
