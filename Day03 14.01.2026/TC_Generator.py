# Generator function to yield numbers 1, 2, and 3
def numbers():
    yield 1
    yield 2
    yield 3

print("----- generator example -----")
gen = numbers()
print(next(gen))
print(next(gen))
print(next(gen))

print("----- iterating using for loop -----")
def count_up(n):
    for i in range(1, n + 1):
        yield i
for val in count_up(5):
    print(val)
