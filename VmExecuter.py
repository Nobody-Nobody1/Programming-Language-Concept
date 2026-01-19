from VMPython import VirtualMachine
from ByteCodeReader import Reader as ByteCodeReader


program = 'ByteCode.txt'
memory_registers = 4

bytecode = ByteCodeReader.read_bytecode(program)
vm = VirtualMachine(memory_registers)
output = vm.execute(bytecode, return_output=False)

if output is None:
    print("Done")
else:
    print("Final Registers State:", output)