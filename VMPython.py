import ReadmeInteracter

class VirtualMachine:
    def __init__(self, memory_registers, memory_size):
        self.registers = [0] * memory_registers
        self.pc = 0  # Program Counter
        self.running = True

    def execute (self, bytecode):
        for instruction in bytecode:
            code = instruction[0]
            if code == 'MOVE':
                reg = int(instruction[1])
                val = int(instruction[2])
                self.registers[reg] = val
            
            elif code == 'ADD':
                reg1 = int(instruction[1])
                reg2 = int(instruction[2])
                reg3 = int(instruction[3])
                self.registers[reg3] = self.registers[reg1] + self.registers[reg2]
            
            elif code == 'SUB':
                reg1 = int(instruction[1])
                reg2 = int(instruction[2])
                reg3 = int(instruction[3])
                self.registers[reg3] = self.registers[reg1] - self.registers[reg2]
            
            elif code == 'DIV':
                reg1 = int(instruction[1])
                reg2 = int(instruction[2])
                reg3 = int(instruction[3])
                if self.registers[reg2] != 0:
                    self.registers[reg3] = self.registers[reg1] // self.registers[reg2]
                else:
                    raise ZeroDivisionError("Division by zero in DIV instruction")
            
            elif code == 'MUL':
                reg1 = int(instruction[1])
                reg2 = int(instruction[2])
                reg3 = int(instruction[3])
                self.registers[reg3] = self.registers[reg1] * self.registers[reg2]
            
            elif code == 'PRINT_MEM':
                print (self.registers)
            
            elif code == 'HELP':
                ReadmeInteracter.display_readme()
                break

            elif code == 'HALT':
                self.running = False
                break
        return self.registers