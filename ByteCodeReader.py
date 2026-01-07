class Reader:

    def read_bytecode(file_path):
        with open(file_path, 'r') as f:
            bytecode = []
            for line in f:
                instruction = line.strip().split(',')
                bytecode.append(instruction)
        return bytecode