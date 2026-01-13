a = """Hello
Welcome 
to
python"""
print(a[0])
print(a[-5])
print(a[-1])
print(a)
# Slicing

text = "Python"
print(text[0:3])
print(text[2:])
print(text[:-3])
# String operations
print(a + text)
print("Hi" * 3)
print(text.upper())
print(a.replace("python", "java"))

# Length of string
print(len(a))


# Membership operator
print("a" not in "apple")
s1 = "I am {0} ans I am {1} old".format("hema", 30)
print(s1)

s2 = a.split()
print(s2)
