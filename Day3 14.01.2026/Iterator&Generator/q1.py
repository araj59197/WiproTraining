# 1. Custom Iterator Class (Iterates from 1 to N)
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

iterator = NumberIterator(5)  

print("Using for loop:")
for num in iterator:
    print(num)