import VMPython as vm
from ByteCodeReader import CodeReader as reader

class VmExecuter:
    output = vm.VMPython.execute()
    print(output)