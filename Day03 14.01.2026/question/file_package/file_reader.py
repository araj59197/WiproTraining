from .file_writer import write_numbers_to_file

def read_file_content(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        print(f"Successfully read content from '{filename}'")
        return content
    except FileNotFoundError:
        print(f"Error: File not found - '{filename}' does not exist.")
        return None
    except PermissionError:
        print("Error: Permission denied - Cannot read file.")
        return None
