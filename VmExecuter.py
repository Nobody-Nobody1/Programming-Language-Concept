from VMPython import VirtualMachine
from ByteCodeReader import Reader as ByteCodeReader


program = 'ByteCode.txt'
memory_size = 256
memory_registers = 4

bytecode = ByteCodeReader.read_bytecode(program)
vm = VirtualMachine(memory_registers, memory_size)
output = vm.execute(bytecode)
print(output)