def add(a, b):
    print("Addition of", a, "and", b, "is", a + b)


def sub(a, b):
    return a - b


add(5, 10)
print(sub(10, 5))


# Example of function with default parameters
def hello(greeting="Hello", name="User"):
    print("%s, %s" % (greeting, name))


hello()
hello("greetings", "Ram")


# Example of function with variable number of arguments
def print_params(*params):
    print(params)


print_params("testing")
print_params(1, 2, 3, 4, 5)


# Example of function with variable number of keyword arguments
def print_param1s(**params):
    print(params)


print_param1s(x=1, y=2, z=3)
