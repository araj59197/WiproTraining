try:
    a = 10
    b = 0
    print(a / b)
except ZeroDivisionError:
    print("Cannot divide by zero")


try:
    x = int(input("Enter a number: "))
    print(10 / x)
except ValueError:
    print("Invalid input! Please enter a valid integer.")
except ZeroDivisionError:
    print("Cannot divide by zero")
else:
    print("No exceptions occurred.")