from ByteCodeReader import Reader

bytecode = Reader.read_file_lines('ByteCode.txt')
output = Reader.find_in_nested_list(bytecode)

class Commands:
    ADD = 'ADD'
    SUB = 'SUBTRACT'
    MUL = 'MULIPLY'
    DIV = 'DIVIDE'
    STORE = 'STORE'
    PRINT = 'PRINT'
class VMPython:
    def execute():

        Registers = {}
        

        for instruction in bytecode:

            instruction_name = instruction[0].upper()

            if instruction_name == Commands.ADD:
                pass

            elif instruction_name == Commands.SUB:
                pass

            elif instruction_name == Commands.MUL:
                pass

            elif instruction_name == Commands.DIV:
                pass

            elif instruction_name == Commands.STORE:
                register = instruction[1]
                value = instruction[2]
                if value in Registers: #checks if the value is in registers
                    value = Registers[value]
                Registers.update({register: value})
            
            elif instruction_name == Commands.PRINT:
                value = instruction[1]
                if value == 'registers_debug': #checks for special print command
                    print(Registers)
                elif value in Registers: #checks if the value is in registers
                    print(Registers[value])
                
                
