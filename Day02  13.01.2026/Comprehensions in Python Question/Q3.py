# Dictionary Comprehension: Key is number, Value is its cube
numbers = [2, 3, 5, 7, 11]
cubes = {num: num**3 for num in numbers}
print("Cubes of specific numbers:", cubes)
