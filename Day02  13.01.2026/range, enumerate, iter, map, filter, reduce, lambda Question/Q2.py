#2. Uses filter() with a lambda to select only even numbers
numbers = range(1, 21)

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

print(even_numbers)