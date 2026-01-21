from ByteCodeReader import CodeReader as reader
bytecode = reader.read_file_lines('ByteCode.txt')
class VMPython:

    def execute():
        registers = {}
        for line in bytecode.values():
            if line[0] == 'PRINT':
                text = line[1]
                print(text)
            elif line [0] == 'MOVE':
                reg = line[1]
                val = int(line[2])
                registers[reg] = val
