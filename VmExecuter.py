import VMPython #command list or dictionary
import ByteCodeReader #converts file into commands

vm = VMPython.SimpleVM()
file = 'ByteCode.txt'
bytecode = ByteCodeReader.read_text_file_to_list(file)

output = vm.execute(bytecode)
print (output)