# 3. Demonstration of Iterator vs Generator

class NumberIterator:
    def __init__(self, limit):
        self.limit = limit
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.limit:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

def fib_generator(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

N = 5

print("--- Iterator Output ---")
num_iter = NumberIterator(N)
for num in num_iter:
    print(num, end=" ")
print() 

print("\n--- Generator Output ---")
fib_gen = fib_generator(N)
for fib in fib_gen:
    print(fib, end=" ")
print()
