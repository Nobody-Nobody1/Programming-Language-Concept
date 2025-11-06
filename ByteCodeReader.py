def read_text_file_to_list():
    lines_list = []
    filepath = '/workspaces/Virtual-Machine/ByteCode.txt'
    try:
        with open(filepath, 'r') as file:
            for line in file:
                lines_list.append(line.strip())  # Remove leading/trailing whitespace, including newline
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return lines_list

content_array = read_text_file_to_list()
print (content_array)