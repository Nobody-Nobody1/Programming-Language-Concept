import VMPython
import ByteCodeReader

vm = VMPython.SimpleVM()
file = '/workspaces/Virtual-Machine/ByteCode.txt'
bytecode = ByteCodeReader.read_text_file_to_list(file)

vm.execute(bytecode)
print(vm.stack)