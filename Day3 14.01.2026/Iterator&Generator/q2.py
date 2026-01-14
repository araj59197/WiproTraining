# 2. Generator Function (Yields first N Fibonacci numbers)
def fib_generator(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1
iterator = fib_generator(5)  

print("Using for loop:")
for num in iterator:
    print(num)