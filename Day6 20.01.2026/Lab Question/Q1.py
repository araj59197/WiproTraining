# Match and search functions, Regular expression patterns, Meta-characters, Special sequences                        
                        
# Write a Python program that:                        
                        
# 1. Uses re.match() to check whether a string starts with a valid employee ID in the format EMP followed by 3 digits (e.g., EMP123)                        
                        
# 2. Uses re.search() to find the first occurrence of a valid email address in a given text                        
                        
# 3. Demonstrates the use of meta-characters (., *, +, ?) and special sequences (\d, \w, \s) in the patterns                        
                        
# 4. Prints matched groups using capturing parentheses 

import re


emp_id_input = "EMP789"

emp_id_regex = r"^(EMP)([0-9]{3})"

emp_match = re.match(emp_id_regex, emp_id_input)

if emp_match:
    print("Employee ID is valid")
    print("Complete ID:", emp_match.group())
    print("Code:", emp_match.group(1))
    print("Number:", emp_match.group(2))
else:
    print("Employee ID is invalid")

print("-" * 50)


message = "For queries, email hr.department_01@company.co.in anytime."

email_regex = r"([\w\.]+)@([\w]+)\.(\w+)(?:\.\w+)?"

email_search = re.search(email_regex, message)

if email_search:
    print("Email detected")
    print("Email:", email_search.group(0))
    print("User name:", email_search.group(1))
    print("Domain name:", email_search.group(2))
    print("Extension:", email_search.group(3))
else:
    print("No email detected")

print("-" * 50)
info = "ItemA   120 units"

pattern = r"(\w+)\s+(\d+)\s*(units?)"
# \w  -> word characters
# \d  -> digits
# \s  -> spaces
# +   -> one or more
# *   -> zero or more
# ?   -> optional character

result = re.search(pattern, info)

if result:
    print("Data matched successfully")
    print("Item Name:", result.group(1))
    print("Quantity:", result.group(2))
    print("Unit:", result.group(3))
