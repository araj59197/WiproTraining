# lambda -> anonymous function
# syntax -> lambda arguments: expression
lambda_add = lambda a, b: a + b
result = lambda_add(10, 20)
print(result)


multi = lambda x, y: x * y
print(multi(5, 4))

maximum = lambda a, b: a if a > b else b
print(maximum(10, 20))


#map(function,iteratble)
numbers=[1,2,3,4,5]
result=map(lambda x:x*2,numbers)
print(list(result))