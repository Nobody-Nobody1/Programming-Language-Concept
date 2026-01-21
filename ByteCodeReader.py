class CodeReader:
    def read_file_lines(file_path):
        output = {}
        with open(file_path, "r") as file:
            lines = file.readlines()
            for index, line in enumerate(lines):
                output[index] = line.strip().split(' ')
        return output