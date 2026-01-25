class Reader:
    def read_file_lines(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return [line.strip().split(' ') for line in lines]

    def find_in_nested_list(nested_list):
        if not isinstance(nested_list, list):
            raise TypeError("nested_list must be a list of lists")

        positions = []
        for row_index, row in enumerate(nested_list):
            if not isinstance(row, list):
                continue  # Skip non-list elements
            for col_index, value in enumerate(row):
                    positions.append((row_index, col_index,value))
        return positions