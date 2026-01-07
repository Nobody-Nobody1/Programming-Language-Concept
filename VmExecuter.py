from VMPython import VirtualMachine


program = 'ByteCode.txt'
memory_size = 256
memory_registers = 16


vm = VirtualMachine()
output = vm.execute(program, memory_size, memory_registers)
print(output)