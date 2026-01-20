# Question – Assertions & Regular Expression Modifiers

# Topics Covered:
# Assertions, Regular expression modifiers

# Write a Python program that:

# 1. Validates a strong password using regular expressions with the following rules:


# Minimum 8 characters

# At least one uppercase letter

# At least one lowercase letter

# At least one digit

# At least one special character

# 2. Uses lookahead assertions (?=)

# 3. Uses regular expression modifiers such as:
# re.IGNORECASE

# re.MULTILINE

# re.DOTALL

# 4. Demonstrates how modifiers affect pattern matching with examples
import re


def is_strong_password(pwd: str) -> bool:
    pattern = r"""
        ^(?=.*[A-Z])
         (?=.*[a-z])
         (?=.*\d)
         (?=.*[^\w\s])
         .{8,}$
    """
    return re.match(pattern, pwd, re.VERBOSE) is not None


passwords = [
    "Abc@1234",
    "abc@1234",
    "ABC@1234",
    "Abc@abcd",
    "Abc12345",
    "A@1a",
]

print("=== Strong Password Validation ===")
for p in passwords:
    print(f"{p:<12} -> {'STRONG' if is_strong_password(p) else 'WEAK'}")

print("\n" + "=" * 50 + "\n")


print("=== IGNORECASE Demo ===")
text1 = "Hello hELLo heLLo"
pattern1 = r"hello"

print("Without IGNORECASE:", re.findall(pattern1, text1))
print("With IGNORECASE   :", re.findall(pattern1, text1, flags=re.IGNORECASE))

print("\n" + "-" * 50 + "\n")


print("=== MULTILINE Demo ===")
text2 = "ERROR: first issue\nINFO: ok\nERROR: second issue\nwarning: low memory"
pattern2 = r"^ERROR:.*$"

print("Without MULTILINE:", re.findall(pattern2, text2))
print("With MULTILINE   :", re.findall(pattern2, text2, flags=re.MULTILINE))

print("\n" + "-" * 50 + "\n")


print("=== DOTALL Demo ===")
text3 = "Start\nMiddle line\nEnd"
pattern3 = r"Start.*End"

print("Without DOTALL:", "MATCH" if re.search(pattern3, text3) else "NO MATCH")
print(
    "With DOTALL   :",
    "MATCH" if re.search(pattern3, text3, flags=re.DOTALL) else "NO MATCH",
)

print("\n" + "-" * 50 + "\n")


print("=== Combined Flags Demo ===")
text4 = "Error: a\nERROR: b\nerror: c\nOk: done"
pattern4 = r"^error:.*$"

print(re.findall(pattern4, text4, flags=re.IGNORECASE | re.MULTILINE))
