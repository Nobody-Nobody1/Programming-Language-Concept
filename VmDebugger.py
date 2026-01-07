from ByteCodeReader import Reader as ByteCodeReader

file = 'ByteCode.txt'
bytecode = ByteCodeReader.read_bytecode(file)

print(bytecode) #prints the array of bytecode instructions