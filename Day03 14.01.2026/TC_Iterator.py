data = [1, 2, 3, 4, 5]
iterator = iter(data)

print("----- iterator example -----")
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))

print("-----iterating using for loop -----")
for x in [10, 20, 30]:
    print(x)


# custom iterator
print("----- custom iterator -----")
class count:
    def __init__(self, limit):
        self.limit = limit
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.limit:
            val = self.current
            self.current += 1
            return val
        else:
            raise StopIteration


obj = count(5)
for num in obj:
    print(num)
