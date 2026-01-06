class VirtualMachine:
    def __init__(self, memory_size=256):
        self.registers = [0] * 4  # R0, R1, R2, R3
        self.memory = [0] * memory_size
        self.pc = 0  # Program Counter
        self.running = True

    def load_program(self, program):
        if len(program) > len(self.memory):
            raise ValueError("Program too large for memory.")
        self.memory[:len(program)] = program

    def fetch(self):
        if self.pc >= len(self.memory):
            raise RuntimeError("Program counter out of bounds.")
        byte = self.memory[self.pc]
        self.pc += 1
        return byte

    def run(self):
        while self.running:
            opcode = self.fetch()

            if opcode == 0x01:  # LOAD reg, value
                reg = self.fetch()
                value = self.fetch()
                self.registers[reg] = value

            elif opcode == 0x02:  # ADD reg1, reg2
                r1 = self.fetch()
                r2 = self.fetch()
                self.registers[r1] = (self.registers[r1] + self.registers[r2]) & 0xFF  # 8-bit wrap

            elif opcode == 0x03:  # STORE reg, addr
                reg = self.fetch()
                addr = self.fetch()
                if addr >= len(self.memory):
                    raise RuntimeError("Memory address out of range.")
                self.memory[addr] = self.registers[reg]

            elif opcode == 0x04:  # JMP addr
                addr = self.fetch()
                if addr >= len(self.memory):
                    raise RuntimeError("Jump address out of range.")
                self.pc = addr

            elif opcode == 0xFF:  # HALT
                self.running = False

            else:
                raise RuntimeError(f"Unknown opcode: {opcode:#04x}")

    def dump_state(self):
        """Print registers and first 16 bytes of memory."""
        print("Registers:", self.registers)
        print("Memory[0:16]:", self.memory[:16])