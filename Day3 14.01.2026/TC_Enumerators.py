# --- Using Enumerate in Python ---
# The enumerate() function adds a counter to an iterable and returns it as an enumerate object.
fruits = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
for index, fruit in enumerate(fruits):
    print(f"Index {index}: {fruit}")
print("\nStarting enumeration from index 1:")


from enum import Enum
class color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
print(color.RED.value)
print(color.GREEN.name)
