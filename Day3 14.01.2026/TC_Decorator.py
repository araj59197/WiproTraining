def mydecorator(func):
    def wrapper():
        print("Before calling the function")
        func()
        print("After calling the function")
    return wrapper
@mydecorator
def say_hello():
    print("Hello, World!")
say_hello()