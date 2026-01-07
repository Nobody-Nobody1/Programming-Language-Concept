from VMPython import VirtualMachine
from ByteCodeReader import Reader as ByteCodeReader


program = 'ByteCode.txt'
memory_size = 256
memory_registers = 16

bytecode = ByteCodeReader.read_bytecode(program)
vm = VirtualMachine()
output = vm.execute(bytecode)
print(output)