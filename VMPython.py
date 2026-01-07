class VirtualMachine:
    def __init__(self):
        self.registers = [0] * 4
        self.memory = [0] * 256
        self.pc = 0  # Program Counter
        self.running = True

    def execute (self, bytecode):
        for instruction in bytecode:
            op = instruction[0]
            if op == 'MOVE':
                reg = int(instruction[1])  # Assuming register format is R0, R1, etc.
                val = int(instruction[2])
                self.registers[reg] = val
            elif op == 'ADD':
                reg1 = int(instruction[1])
                reg2 = int(instruction[2])
                reg3 = int(instruction[3])
                self.registers[reg3] = self.registers[reg1] + self.registers[reg2]
        return self.registers