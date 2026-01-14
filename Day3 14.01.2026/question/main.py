# Question: Functions, Modules, File Handling & Exceptions
# Topic: Functions, Modules (package), File Handling, Exceptions
#
# Create a small Python package with:
# 1. A module containing a function write_numbers_to_file(filename)
# 2. The function should write numbers 1-100 into a file
# 3. Handle possible exceptions such as:
#    - File not found
#    - Permission denied
# 4. Create another module that imports this function and reads the file content safely

from file_package import write_numbers_to_file, read_file_content

# Write numbers 1-100 to file
write_numbers_to_file("numbers.txt")

content = read_file_content("numbers.txt")
if content:
    print("\nFile Content:")
    print(content)

print("\n--- Testing Exception Handling ---")
read_file_content("non_existent_file.txt")
write_numbers_to_file("Z:/invalid_path/file.txt")
