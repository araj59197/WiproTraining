numbers = [1, 2, 3, 4, 5]
names = ["Ram", "Hari", "Ramaya"]
mixed = [1, "Python", 3.5, True]

numbers[1] = 100
print(numbers)
print(names)
print(mixed)

for i in numbers:
    print(i)
    
if 10 in numbers:
    print("Found")
    
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(matrix[1][2])