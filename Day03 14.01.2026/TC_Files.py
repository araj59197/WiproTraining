file = open("f1.txt", "r")
content = file.readline()
content1 = file.readlines()
print(content)
print(content1)
file.close()

file = open("f1.txt", "a")
file.write("\nlets learn python")
file.write("\nThis is my write example")
file.close()

# Read and Write both using r+ mode
print("\n--- Using r+ mode (read and write both) ---")
file = open("f1.txt", "r+")
print("Reading first:", file.read())
file.write("\nNew line added with r+ mode")
file.close()

# Read again to see changes
print("\n--- After writing ---")
file = open("f1.txt", "r")
print(file.read())
file.close()