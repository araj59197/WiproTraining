# Tuple in Python
# Creating tuples
t1 = (10, 20, 30, 40, 50)
t2 = "apple", "orange", "cherry"
print(t1[0])
print(t2[2])
print(t1[1:3])
print(t1[:2])
print(t1[3:])
# t1[2]=40;
print(t1)
print(t1.count(20))
print(t1.index(40))

# Swap values using tuple unpacking
a = 5
b = 10
a, b = b, a
print(a, b)

# Tuple unpacking
data = (10, 20, 30)
a, b, c = data
print(a, b, c)