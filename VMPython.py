from ByteCodeReader import Reader

bytecode = Reader.read_file_lines('ByteCode.txt')
output = Reader.find_in_nested_list(bytecode)

class Commands:
    LOAD = 'LOAD'
    ADD = 'ADD'
    SUB = 'SUB'
    MUL = 'MUL'
    DIV = 'DIV'
    STORE = 'STORE'
    PRINT = 'PRINT'
class VMPython:
    def execute():
        for command in output:
            if command[2] == Commands.LOAD:
                location = command[0], command[1]
                print("there is a LOAD command at", location)