# 3. Uses map() with a lambda to square the filtered numbers
numbers = range(1, 21)
evens = filter(lambda x: x % 2 == 0, numbers)

squared_numbers = map(lambda x: x ** 2, evens)

print(list(squared_numbers))