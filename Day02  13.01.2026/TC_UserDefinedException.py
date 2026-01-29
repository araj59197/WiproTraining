class MyError(Exception):
    """Custom exception class for user-defined errors."""

    pass

class InvalidAgeError(Exception):
    """Custom exception for invalid age input."""

    pass

try:
    age = int(input("Enter your age:"))
    if age < 18:
        raise InvalidAgeError("Age must be at least 18.")
    else:
        print("eligible to vote.")
except InvalidAgeError as e:
    print("Error:", e)
