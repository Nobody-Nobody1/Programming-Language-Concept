def read_file_lines(file_path):
    try:
        # Open the file in read mode with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                # Strip newline characters for cleaner output
                clean_line = line.rstrip('\n')
                print(f"Line {line_number}: {clean_line}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: You don't have permission to read '{file_path}'.")
    except UnicodeDecodeError:
        print(f"Error: Could not decode '{file_path}'. Try a different encoding.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
# Replace 'example.txt' with your file path
read_file_lines('example.txt')
