# Set Comprehension: Store only unique even numbers
numbers = [1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 10]
unique_evens = {num for num in numbers if num % 2 == 0}
print("Unique even numbers:", unique_evens)