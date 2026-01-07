class VirtualMachine:
    def __init__(self, memory_size, memory_registers):
        self.registers = [0] * memory_registers
        self.memory = [0] * memory_size
        self.pc = 0  # Program Counter
        self.running = True

    def execute (self, bytecode):
        with open(bytecode, 'r') as f:
            program = [int(line.strip(), 16) for line in f if line.strip()]

        while self.running and self.pc < len(program):
            opcode = program[self.pc]

            if opcode == "LOAD":  # LOAD
                reg = program[self.pc + 1]
                value = program[self.pc + 2]
                self.registers[reg] = value
                self.pc += 3

            elif opcode == "ADD":  # ADD
                reg1 = program[self.pc + 1]
                reg2 = program[self.pc + 2]
                self.registers[reg1] += self.registers[reg2]
                self.pc += 3

            elif opcode == "STORE":  # STORE
                reg = program[self.pc + 1]
                addr = program[self.pc + 2]
                self.memory[addr] = self.registers[reg]
                self.pc += 3

            elif opcode == "HALT":  # HALT
                self.running = False
                self.pc += 1
            
            else:
                print(f"Unknown opcode {opcode} at address {self.pc}")
                self.running = False