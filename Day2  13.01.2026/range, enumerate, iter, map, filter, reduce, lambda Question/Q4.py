# 4. Uses reduce() to calculate the sum of squared even numbers
from functools import reduce

squared_evens = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, range(1, 21))))

total_sum = reduce(lambda a, b: a + b, squared_evens)

print(total_sum)