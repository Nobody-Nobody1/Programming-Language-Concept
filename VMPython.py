from ByteCodeReader import CodeReader as reader

class VMPython:
    input = 'ByteCode.txt'
    output = reader.read_file_lines(input)
    print(output)