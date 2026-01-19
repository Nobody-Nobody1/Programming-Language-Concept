import ReadmeInteracter
from ByteCodeReader import Reader

class VirtualMachine:
    def __init__(self, memory_registers):
        self.registers = [0] * memory_registers # memory_registers is the amount of registers
        self.executed_instructions = 0


    def execute (self, bytecode, return_output=False, debug=False):
        for instruction in bytecode:
            code = instruction[0]

            # data movement
            if code == 'MOVE':
                reg = int(instruction[1])
                val = int(instruction[2])
                self.registers[reg] = val
                self.executed_instructions += 1
            
            # mathematical operations
            elif code == 'ADD': 
                reg1 = int(instruction[1])
                reg2 = int(instruction[2])
                reg3 = int(instruction[3])
                self.registers[reg3] = self.registers[reg1] + self.registers[reg2]
                self.executed_instructions += 1
            
            elif code == 'SUBTRACT':
                reg1 = int(instruction[1])
                reg2 = int(instruction[2])
                reg3 = int(instruction[3])
                self.registers[reg3] = self.registers[reg1] - self.registers[reg2]
                self.executed_instructions += 1
            
            elif code == 'DIVIDE':
                reg1 = int(instruction[1])
                reg2 = int(instruction[2])
                reg3 = int(instruction[3])
                if self.registers[reg2] != 0:
                    self.registers[reg3] = self.registers[reg1] // self.registers[reg2]
                    self.executed_instructions += 1
                else:
                    raise ZeroDivisionError("Division by zero in DIV instruction")
            
            elif code == 'MULITIPLY':
                reg1 = int(instruction[1])
                reg2 = int(instruction[2])
                reg3 = int(instruction[3])
                self.registers[reg3] = self.registers[reg1] * self.registers[reg2]
                self.executed_instructions += 1
            
            # output and debugging
            elif code == 'PRINT_MEMORY':
                print (self.registers)
                self.executed_instructions += 1
            
            elif code == 'PRINT_ARRAY':
                input = Reader.read_bytecode('ByteCode.txt')
                print (input)
                self.executed_instructions += 1

            elif code == 'PRINT_EXECUTED':
                print (f"Executed Instructions: {self.executed_instructions}")
                self.executed_instructions += 1

            # help command

            elif code == 'HELP':
                ReadmeInteracter.display_readme()
                break

            #program flow

            elif code == 'HALT':
                break

            elif code == 'NOOP':
                continue
            self.executed_instructions += 1
                
        if return_output and debug:
            return self.registers, self.executed_instructions, 
        elif return_output:
            return self.registers