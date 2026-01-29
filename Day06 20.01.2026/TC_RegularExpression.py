import re

text = "python is powerful."
result = re.match(r"java", text)
if result:
    print("Match found:", result.group())
else:
    print("No match found.")
searchResult = re.search("powerful", text)
print("Search result:", searchResult.group())
print(searchResult.start())
print(searchResult.end())

email = "admin@gmail.com"
if re.match(r"[a-zA-Z]+@", email):
    print("Valid Start")
result2 = re.fullmatch(r"\d{10}", "1234567890")
print("Full match result:", result2)

print(re.findall(r"\d+", "price 50 and 100 and 200"))

for n in re.finditer(r"\d+", "A1, B33, C444"):
    print(n.group(), n.start(), n.end())

print(re.search(r"\d+", "Age is 25"))

print(re.search(r"^a.*c$", "abnkkkkkknnc"))

print(n.group())

# re.I ensures case-insensitive matching ("python" matches "Python")
print(re.search("python", "Python", re.I))

# re.M enables multiline matching, allowing ^ to match the start of each line
text4 = "one\ntwo\nthree"
print(re.findall(r"^t\w+", text4, re.M))
