def write_numbers_to_file(filename):
    try:
        with open(filename, 'w') as file:
            for num in range(1, 101):
                file.write(f"{num}\n")
        print(f"Successfully wrote numbers 1-100 to '{filename}'")
        return True
    except FileNotFoundError:
        print("Error: File not found - The directory path doesn't exist.")
        return False
    except PermissionError:
        print("Error: Permission denied - Cannot write to file.")
        return False
