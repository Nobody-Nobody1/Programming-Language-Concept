class CodeReader:
    def read_file_lines(file_path):
        for line_number, line in enumerate(open(file_path, 'r')):
            line = line.strip().split(' ')
            return line, line_number