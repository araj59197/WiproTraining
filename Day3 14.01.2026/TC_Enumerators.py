# --- Using Enumerate in Python ---
# The enumerate() function adds a counter to an iterable and returns it as an enumerate object.
fruits = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
for index, fruit in enumerate(fruits):
    print(f"Index {index}: {fruit}")
print("\nStarting enumeration from index 1:")
for index, fruit in enumerate(fruits, start=1):
    print(f"Index {index}: {fruit}")
print("\nCreating a dictionary from enumerated fruits:")
fruit_dict = dict(enumerate(fruits))
print(fruit_dict)
