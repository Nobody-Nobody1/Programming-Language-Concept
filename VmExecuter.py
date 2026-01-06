from VMPython import VirtualMachine


# Example program:
# R0 = 10
# R1 = 20
# R0 = R0 + R1
# STORE R0 into memory[10]
# HALT
program = [
    0x01, 0x00, 0x0A,  # LOAD R0, 10
    0x01, 0x01, 0x14,  # LOAD R1, 20
    0x02, 0x00, 0x01,  # ADD R0, R1
    0x03, 0x00, 0x0A,  # STORE R0, 10
    0xFF               # HALT
]

if __name__ == "__main__":
    vm = VirtualMachine()
    vm.load_program(program)
    vm.run()
    vm.dump_state()