def read_text_file_to_list(filepath):
    lines_list = []

    try:
        with open(filepath, 'r') as file:
            for line in file:
                lines_list.append(line.strip())
                if line.strip().isdigit():
                    lines_list[-1] = int(line.strip())
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return lines_list