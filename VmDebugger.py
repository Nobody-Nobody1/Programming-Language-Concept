import ByteCodeReader #converts file into commands

file = '/workspaces/Virtual-Machine/ByteCode.txt'
bytecode = ByteCodeReader.read_text_file_to_list(file)

print(bytecode) #prints the array of bytecode instructions